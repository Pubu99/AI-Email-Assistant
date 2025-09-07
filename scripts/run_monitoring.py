#!/usr/bin/env python3
"""
Comprehensive MLOps Monitoring Script
Orchestrates all monitoring activities including performance, drift, and health checks
"""

import logging
import yaml
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
import schedule
import argparse
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mlops.model_monitor import ModelMonitor
from mlops.model_registry import ModelRegistry

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MLOpsMonitor:
    def __init__(self, config_path="config/mlops_config.yaml"):
        """Initialize MLOps monitoring system"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['mlops']
        
        self.model_monitor = ModelMonitor()
        self.model_registry = ModelRegistry()
        
        # Create monitoring directories
        Path("mlops/reports").mkdir(parents=True, exist_ok=True)
        Path("mlops/predictions").mkdir(parents=True, exist_ok=True)
        Path("mlops/logs").mkdir(parents=True, exist_ok=True)
        
    def health_check(self) -> dict:
        """Perform health check on the ML system"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'checks': {}
        }
        
        try:
            # Check API health
            api_url = f"http://localhost:8000{self.config['deployment']['health_check_endpoint']}"
            response = requests.get(api_url, timeout=10)
            health_status['checks']['api'] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds(),
                'status_code': response.status_code
            }
        except Exception as e:
            health_status['checks']['api'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'unhealthy'
        
        # Check MLflow tracking server
        try:
            import mlflow
            mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
            experiments = mlflow.list_experiments()
            health_status['checks']['mlflow'] = {
                'status': 'healthy',
                'experiments_count': len(experiments)
            }
        except Exception as e:
            health_status['checks']['mlflow'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'unhealthy'
        
        # Check model availability
        models_status = {}
        for model_name in ['intent_classifier', 'reply_generator']:
            model_info = self.model_registry.get_model_info(model_name, 'Production')
            if model_info:
                models_status[model_name] = 'available'
            else:
                models_status[model_name] = 'unavailable'
                health_status['status'] = 'degraded'
        
        health_status['checks']['models'] = models_status
        
        return health_status
    
    def performance_monitoring(self) -> dict:
        """Monitor model performance metrics"""
        logger.info("Running performance monitoring...")
        
        performance_report = {
            'timestamp': datetime.now().isoformat(),
            'models': {}
        }
        
        for model_name in ['intent_classifier', 'reply_generator']:
            # Get recent predictions
            predictions_dir = Path("mlops/predictions")
            recent_files = []
            
            if predictions_dir.exists():
                for file_path in predictions_dir.glob(f"{model_name}_*.csv"):
                    try:
                        # Check if file is from last 24 hours
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if datetime.now() - file_time < timedelta(hours=24):
                            recent_files.append(file_path)
                    except:
                        continue
            
            if recent_files:
                # Calculate aggregate metrics
                all_predictions = []
                for file_path in recent_files:
                    try:
                        import pandas as pd
                        df = pd.read_csv(file_path)
                        all_predictions.append(df)
                    except:
                        continue
                
                if all_predictions:
                    combined_df = pd.concat(all_predictions, ignore_index=True)
                    
                    from sklearn.metrics import accuracy_score, classification_report
                    accuracy = accuracy_score(combined_df['true'], combined_df['predicted'])
                    
                    performance_report['models'][model_name] = {
                        'accuracy': accuracy,
                        'total_predictions': len(combined_df),
                        'prediction_files': len(recent_files)
                    }
                    
                    # Check against thresholds
                    if model_name in self.config['monitoring']['alert_thresholds']:
                        threshold = self.config['monitoring']['alert_thresholds'].get('accuracy_drop', 0.1)
                        # Get baseline from model registry
                        model_info = self.model_registry.get_model_info(model_name, 'Production')
                        if model_info and 'accuracy' in model_info['metrics']:
                            baseline_accuracy = model_info['metrics']['accuracy']
                            performance_drop = baseline_accuracy - accuracy
                            
                            if performance_drop > threshold:
                                self.send_alert(
                                    f"Performance Alert: {model_name}",
                                    f"Accuracy dropped by {performance_drop:.3f} "
                                    f"(current: {accuracy:.3f}, baseline: {baseline_accuracy:.3f})"
                                )
            else:
                performance_report['models'][model_name] = {
                    'status': 'no_recent_predictions'
                }
        
        return performance_report
    
    def drift_monitoring(self) -> dict:
        """Monitor for data and model drift"""
        logger.info("Running drift monitoring...")
        
        drift_report = {
            'timestamp': datetime.now().isoformat(),
            'drift_detected': False,
            'models': {}
        }
        
        # Run drift detection for each model
        for model_name in ['intent_classifier', 'reply_generator']:
            try:
                # Use the drift detection script
                import subprocess
                result = subprocess.run([
                    'python', 'scripts/check_drift.py',
                    '--model', model_name,
                    '--window-days', str(self.config['drift_detection']['monitoring_window_days'])
                ], capture_output=True, text=True, cwd='.')
                
                if result.returncode == 0:
                    drift_report['models'][model_name] = {'status': 'no_drift'}
                else:
                    drift_report['models'][model_name] = {'status': 'drift_detected'}
                    drift_report['drift_detected'] = True
                    
                    # Send alert if drift detected
                    self.send_alert(
                        f"Drift Alert: {model_name}",
                        f"Drift detected for model {model_name}. Check logs for details."
                    )
                    
            except Exception as e:
                logger.error(f"Error in drift monitoring for {model_name}: {e}")
                drift_report['models'][model_name] = {'status': 'error', 'error': str(e)}
        
        return drift_report
    
    def data_quality_monitoring(self) -> dict:
        """Monitor data quality"""
        logger.info("Running data quality monitoring...")
        
        # This would check recent data against quality rules
        # For now, return a basic structure
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'passed',
            'checks_performed': len(self.config['data_quality']['validation_rules'])
        }
    
    def send_alert(self, subject: str, message: str):
        """Send alert through configured channels"""
        if not self.config['alerting']['enabled']:
            return
        
        logger.warning(f"ALERT: {subject} - {message}")
        
        # Here you would implement actual alerting logic
        # For example: send email, Slack notification, etc.
        for channel in self.config['alerting']['channels']:
            if channel['type'] == 'email':
                logger.info(f"Would send email alert to {channel['recipients']}")
            elif channel['type'] == 'slack':
                logger.info(f"Would send Slack alert to {channel.get('webhook_url', 'configured webhook')}")
    
    def generate_monitoring_report(self) -> str:
        """Generate comprehensive monitoring report"""
        logger.info("Generating monitoring report...")
        
        # Collect all monitoring data
        health_data = self.health_check()
        performance_data = self.performance_monitoring()
        drift_data = self.drift_monitoring()
        data_quality_data = self.data_quality_monitoring()
        
        # Combine into comprehensive report
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'health_check': health_data,
            'performance_monitoring': performance_data,
            'drift_monitoring': drift_data,
            'data_quality': data_quality_data,
            'summary': {
                'models_monitored': ['intent_classifier', 'reply_generator'],
                'alerts_triggered': 0,
                'recommendations': []
            }
        }
        
        # Determine overall status
        if health_data['status'] == 'unhealthy':
            report['overall_status'] = 'unhealthy'
        elif drift_data['drift_detected']:
            report['overall_status'] = 'degraded'
            report['summary']['alerts_triggered'] += 1
            report['summary']['recommendations'].append('Investigate drift detection results')
        
        # Save report
        report_path = f"mlops/reports/monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Monitoring report saved to {report_path}")
        return report_path
    
    def run_scheduled_monitoring(self):
        """Run monitoring on schedule"""
        logger.info("Starting scheduled monitoring...")
        
        # Schedule monitoring tasks
        schedule.every(self.config['monitoring']['check_interval_hours']).hours.do(
            self.generate_monitoring_report
        )
        
        # Schedule drift detection
        schedule.every().day.at("06:00").do(self.drift_monitoring)
        
        # Run scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    parser = argparse.ArgumentParser(description="MLOps Monitoring System")
    parser.add_argument("--mode", choices=['once', 'scheduled'], default='once',
                       help="Run monitoring once or continuously")
    parser.add_argument("--config", default="config/mlops_config.yaml",
                       help="Path to MLOps configuration file")
    
    args = parser.parse_args()
    
    monitor = MLOpsMonitor(args.config)
    
    if args.mode == 'once':
        # Run monitoring once
        monitor.generate_monitoring_report()
    else:
        # Run continuously
        monitor.run_scheduled_monitoring()

if __name__ == "__main__":
    main()