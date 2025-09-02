import mlflow
import logging
from datetime import datetime
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

class ModelMonitor:
    def __init__(self):
        mlflow.set_tracking_uri("sqlite:///mlops/mlruns.db")
        self.experiment_name = "email_assistant"
        mlflow.set_experiment(self.experiment_name)
        
    def log_metrics(self, model_name, metrics):
        """Log model performance metrics to MLflow"""
        with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M')}"):
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)
                
    def monitor_predictions(self, y_true, y_pred, model_name):
        """Monitor model predictions and log performance metrics"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'timestamp': datetime.now().timestamp()
        }
        
        # Get detailed classification report
        report = classification_report(y_true, y_pred, output_dict=True)
        
        # Log metrics
        self.log_metrics(model_name, metrics)
        
        # Save predictions for drift detection
        pred_df = pd.DataFrame({
            'true': y_true,
            'predicted': y_pred,
            'timestamp': datetime.now()
        })
        pred_df.to_csv(f'mlops/predictions/{model_name}_{datetime.now().strftime("%Y%m%d")}.csv', 
                       index=False)
        
    def detect_drift(self, model_name, window_size=7):
        """Detect model performance drift"""
        files = sorted(glob.glob(f'mlops/predictions/{model_name}_*.csv'))[-window_size:]
        if len(files) < 2:
            return False
            
        accuracies = []
        for f in files:
            df = pd.read_csv(f)
            acc = accuracy_score(df['true'], df['predicted'])
            accuracies.append(acc)
            
        # Check if recent performance is significantly worse
        baseline = np.mean(accuracies[:-1])
        current = accuracies[-1]
        
        if current < baseline - 0.1:  # 10% degradation threshold
            logging.warning(f"Performance drift detected for {model_name}")
            return True
        return False
