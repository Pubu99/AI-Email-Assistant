#!/usr/bin/env python3
"""
Data and Model Drift Detection Script
Monitors for distribution changes in input data and model performance degradation
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from scipy import stats
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import argparse
import yaml
from pathlib import Path
import mlflow

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DriftDetector:
    def __init__(self, config_path="config/training_config.yaml"):
        """Initialize drift detector with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Thresholds for drift detection
        self.data_drift_threshold = 0.05  # p-value threshold for statistical tests
        self.performance_drift_threshold = 0.1  # 10% performance drop
        
    def detect_data_drift(self, reference_data, current_data, feature_columns):
        """
        Detect data drift using Kolmogorov-Smirnov test for numerical features
        and Chi-square test for categorical features
        """
        drift_results = {}
        
        for column in feature_columns:
            if column in reference_data.columns and column in current_data.columns:
                ref_values = reference_data[column].dropna()
                cur_values = current_data[column].dropna()
                
                if len(ref_values) == 0 or len(cur_values) == 0:
                    continue
                
                # Determine if numerical or categorical
                if pd.api.types.is_numeric_dtype(ref_values):
                    # KS test for numerical features
                    statistic, p_value = stats.ks_2samp(ref_values, cur_values)
                    test_name = "Kolmogorov-Smirnov"
                else:
                    # Chi-square test for categorical features
                    try:
                        ref_counts = ref_values.value_counts()
                        cur_counts = cur_values.value_counts()
                        
                        # Align indices
                        all_categories = set(ref_counts.index) | set(cur_counts.index)
                        ref_aligned = ref_counts.reindex(all_categories, fill_value=0)
                        cur_aligned = cur_counts.reindex(all_categories, fill_value=0)
                        
                        statistic, p_value = stats.chisquare(cur_aligned, ref_aligned)
                        test_name = "Chi-square"
                    except:
                        continue
                
                drift_detected = p_value < self.data_drift_threshold
                
                drift_results[column] = {
                    'test': test_name,
                    'statistic': statistic,
                    'p_value': p_value,
                    'drift_detected': drift_detected
                }
                
                if drift_detected:
                    logger.warning(f"Data drift detected in feature '{column}' (p-value: {p_value:.4f})")
        
        return drift_results
    
    def detect_model_drift(self, model_name, window_days=7):
        """
        Detect model performance drift by comparing recent performance
        with historical baseline
        """
        # Load recent prediction logs
        predictions_dir = Path("mlops/predictions")
        if not predictions_dir.exists():
            logger.warning("No prediction logs found for drift detection")
            return None
        
        # Get prediction files from the last window_days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        prediction_files = []
        for file_path in predictions_dir.glob(f"{model_name}_*.csv"):
            try:
                # Extract date from filename
                date_str = file_path.stem.split('_')[-1]
                file_date = datetime.strptime(date_str, "%Y%m%d")
                if start_date <= file_date <= end_date:
                    prediction_files.append(file_path)
            except:
                continue
        
        if len(prediction_files) < 2:
            logger.info("Insufficient data for model drift detection")
            return None
        
        # Calculate performance metrics for each day
        daily_metrics = []
        for file_path in sorted(prediction_files):
            df = pd.read_csv(file_path)
            if 'true' in df.columns and 'predicted' in df.columns:
                metrics = {
                    'date': file_path.stem.split('_')[-1],
                    'accuracy': accuracy_score(df['true'], df['predicted']),
                    'precision': precision_score(df['true'], df['predicted'], average='weighted', zero_division=0),
                    'recall': recall_score(df['true'], df['predicted'], average='weighted', zero_division=0),
                    'f1': f1_score(df['true'], df['predicted'], average='weighted', zero_division=0)
                }
                daily_metrics.append(metrics)
        
        if len(daily_metrics) < 2:
            return None
        
        # Compare recent performance with baseline
        baseline_metrics = np.mean([m['accuracy'] for m in daily_metrics[:-1]])
        current_metrics = daily_metrics[-1]['accuracy']
        
        performance_drop = baseline_metrics - current_metrics
        drift_detected = performance_drop > self.performance_drift_threshold
        
        result = {
            'model_name': model_name,
            'baseline_accuracy': baseline_metrics,
            'current_accuracy': current_metrics,
            'performance_drop': performance_drop,
            'drift_detected': drift_detected,
            'threshold': self.performance_drift_threshold
        }
        
        if drift_detected:
            logger.warning(f"Model drift detected for {model_name}: "
                         f"Performance dropped by {performance_drop:.3f} "
                         f"(baseline: {baseline_metrics:.3f}, current: {current_metrics:.3f})")
        
        return result
    
    def generate_drift_report(self, data_drift_results=None, model_drift_results=None):
        """Generate a comprehensive drift detection report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_drift': data_drift_results,
            'model_drift': model_drift_results
        }
        
        # Save report
        report_path = f"mlops/reports/drift_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Drift report saved to {report_path}")
        return report

def main():
    parser = argparse.ArgumentParser(description="Check for data and model drift")
    parser.add_argument("--model", default="intent_classifier", help="Model name to check")
    parser.add_argument("--reference-data", help="Path to reference dataset")
    parser.add_argument("--current-data", help="Path to current dataset")
    parser.add_argument("--window-days", type=int, default=7, help="Window for model drift detection")
    
    args = parser.parse_args()
    
    detector = DriftDetector()
    
    # Check model drift
    model_drift = detector.detect_model_drift(args.model, args.window_days)
    
    # Check data drift if datasets provided
    data_drift = None
    if args.reference_data and args.current_data:
        ref_df = pd.read_csv(args.reference_data)
        cur_df = pd.read_csv(args.current_data)
        
        # Assume text features for email data
        feature_columns = ['email_length', 'word_count', 'sentiment_score']  # Add your actual features
        data_drift = detector.detect_data_drift(ref_df, cur_df, feature_columns)
    
    # Generate report
    report = detector.generate_drift_report(data_drift, model_drift)
    
    # Log to MLflow if drift detected
    drift_detected = False
    if model_drift and model_drift['drift_detected']:
        drift_detected = True
    if data_drift and any(result['drift_detected'] for result in data_drift.values()):
        drift_detected = True
    
    if drift_detected:
        mlflow.set_tracking_uri("sqlite:///mlops/mlruns.db")
        with mlflow.start_run(run_name=f"drift_detection_{datetime.now().strftime('%Y%m%d_%H%M')}"):
            mlflow.log_artifact(f"mlops/reports/drift_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
            mlflow.log_metric("drift_detected", 1)
            if model_drift:
                mlflow.log_metric("performance_drop", model_drift['performance_drop'])

if __name__ == "__main__":
    main()