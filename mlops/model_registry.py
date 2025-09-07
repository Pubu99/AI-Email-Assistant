#!/usr/bin/env python3
"""
Model Registry Management
Handles model versioning, staging, and promotion across environments
"""

import mlflow
import mlflow.sklearn
import mlflow.transformers
from mlflow.tracking import MlflowClient
import logging
from datetime import datetime
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelRegistry:
    def __init__(self, tracking_uri="sqlite:///mlops/mlruns.db"):
        """Initialize MLflow model registry"""
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()
        
    def register_model(self, model_name: str, model_path: str, 
                      metrics: Dict, metadata: Dict = None) -> str:
        """
        Register a new model version in MLflow
        
        Args:
            model_name: Name of the model
            model_path: Path to the trained model
            metrics: Performance metrics
            metadata: Additional metadata
            
        Returns:
            Model version number
        """
        # Start MLflow run
        with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M')}"):
            # Log metrics
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)
            
            # Log metadata as parameters
            if metadata:
                for key, value in metadata.items():
                    mlflow.log_param(key, str(value))
            
            # Log model artifacts
            if "transformers" in model_path.lower():
                # For transformer models
                mlflow.transformers.log_model(
                    transformers_model=model_path,
                    artifact_path="model",
                    registered_model_name=model_name
                )
            else:
                # For sklearn models
                mlflow.sklearn.log_model(
                    sk_model=model_path,
                    artifact_path="model",
                    registered_model_name=model_name
                )
            
            # Get run info
            run = mlflow.active_run()
            
        # Get the latest version
        latest_version = self.client.get_latest_versions(
            model_name, stages=["None"]
        )[0]
        
        logger.info(f"Registered {model_name} version {latest_version.version}")
        return latest_version.version
    
    def promote_model(self, model_name: str, version: str, 
                     stage: str, archive_existing: bool = True) -> bool:
        """
        Promote model to a specific stage
        
        Args:
            model_name: Name of the model
            version: Version to promote
            stage: Target stage (Staging, Production)
            archive_existing: Whether to archive existing models in target stage
            
        Returns:
            Success status
        """
        try:
            # Archive existing models in target stage if requested
            if archive_existing:
                existing_models = self.client.get_latest_versions(
                    model_name, stages=[stage]
                )
                for model in existing_models:
                    self.client.transition_model_version_stage(
                        name=model_name,
                        version=model.version,
                        stage="Archived"
                    )
                    logger.info(f"Archived {model_name} v{model.version}")
            
            # Promote new version
            self.client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage=stage
            )
            
            logger.info(f"Promoted {model_name} v{version} to {stage}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to promote model: {e}")
            return False
    
    def get_model_info(self, model_name: str, stage: str = "Production") -> Dict:
        """Get information about a model in a specific stage"""
        try:
            model_version = self.client.get_latest_versions(
                model_name, stages=[stage]
            )[0]
            
            # Get run details
            run = self.client.get_run(model_version.run_id)
            
            return {
                'name': model_name,
                'version': model_version.version,
                'stage': stage,
                'run_id': model_version.run_id,
                'metrics': run.data.metrics,
                'params': run.data.params,
                'created_timestamp': model_version.creation_timestamp,
                'model_uri': f"models:/{model_name}/{stage}"
            }
        except IndexError:
            logger.warning(f"No model found for {model_name} in {stage} stage")
            return None
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return None
    
    def compare_models(self, model_name: str, 
                      version1: str, version2: str) -> Dict:
        """Compare two model versions"""
        try:
            # Get model version details
            mv1 = self.client.get_model_version(model_name, version1)
            mv2 = self.client.get_model_version(model_name, version2)
            
            # Get run details
            run1 = self.client.get_run(mv1.run_id)
            run2 = self.client.get_run(mv2.run_id)
            
            comparison = {
                'model_name': model_name,
                'version1': {
                    'version': version1,
                    'metrics': run1.data.metrics,
                    'created': mv1.creation_timestamp
                },
                'version2': {
                    'version': version2,
                    'metrics': run2.data.metrics,
                    'created': mv2.creation_timestamp
                },
                'metric_differences': {}
            }
            
            # Calculate metric differences
            for metric in run1.data.metrics:
                if metric in run2.data.metrics:
                    diff = run2.data.metrics[metric] - run1.data.metrics[metric]
                    comparison['metric_differences'][metric] = diff
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing models: {e}")
            return None
    
    def list_models(self, stage: str = None) -> List[Dict]:
        """List all registered models, optionally filtered by stage"""
        models = []
        
        for model in self.client.list_registered_models():
            model_info = {
                'name': model.name,
                'description': model.description,
                'versions': []
            }
            
            for version in model.latest_versions:
                if stage is None or version.current_stage == stage:
                    run = self.client.get_run(version.run_id)
                    version_info = {
                        'version': version.version,
                        'stage': version.current_stage,
                        'metrics': run.data.metrics,
                        'created': version.creation_timestamp
                    }
                    model_info['versions'].append(version_info)
            
            if model_info['versions'] or stage is None:
                models.append(model_info)
        
        return models
    
    def auto_promote_model(self, model_name: str, 
                          performance_threshold: Dict) -> bool:
        """
        Automatically promote model based on performance criteria
        
        Args:
            model_name: Name of the model
            performance_threshold: Dict of metric thresholds
            
        Returns:
            Whether promotion occurred
        """
        # Get latest model in None stage
        try:
            latest_models = self.client.get_latest_versions(
                model_name, stages=["None"]
            )
            if not latest_models:
                logger.info(f"No new models found for {model_name}")
                return False
                
            latest_model = latest_models[0]
            run = self.client.get_run(latest_model.run_id)
            
            # Check if model meets promotion criteria
            meets_criteria = True
            for metric, threshold in performance_threshold.items():
                if metric in run.data.metrics:
                    if run.data.metrics[metric] < threshold:
                        meets_criteria = False
                        logger.info(f"Model {model_name} v{latest_model.version} "
                                  f"does not meet {metric} threshold: "
                                  f"{run.data.metrics[metric]} < {threshold}")
                        break
                else:
                    logger.warning(f"Metric {metric} not found in model metrics")
                    meets_criteria = False
                    break
            
            if meets_criteria:
                # Promote to staging first
                success = self.promote_model(
                    model_name, latest_model.version, "Staging"
                )
                if success:
                    logger.info(f"Auto-promoted {model_name} v{latest_model.version} to Staging")
                return success
            else:
                logger.info(f"Model {model_name} v{latest_model.version} "
                          f"does not meet promotion criteria")
                return False
                
        except Exception as e:
            logger.error(f"Error in auto-promotion: {e}")
            return False
    
    def generate_model_report(self) -> str:
        """Generate a comprehensive model registry report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'models': self.list_models(),
            'summary': {
                'total_models': 0,
                'production_models': 0,
                'staging_models': 0
            }
        }
        
        # Calculate summary statistics
        for model in report['models']:
            report['summary']['total_models'] += 1
            for version in model['versions']:
                if version['stage'] == 'Production':
                    report['summary']['production_models'] += 1
                elif version['stage'] == 'Staging':
                    report['summary']['staging_models'] += 1
        
        # Save report
        report_path = f"mlops/reports/model_registry_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Model registry report saved to {report_path}")
        return report_path

def main():
    """Example usage of ModelRegistry"""
    registry = ModelRegistry()
    
    # Example: Auto-promote models based on performance
    intent_classifier_thresholds = {
        'accuracy': 0.85,
        'f1_score': 0.80
    }
    
    reply_generator_thresholds = {
        'bleu_score': 0.30,
        'rouge_score': 0.25
    }
    
    # Auto-promote if models meet criteria
    registry.auto_promote_model('intent_classifier', intent_classifier_thresholds)
    registry.auto_promote_model('reply_generator', reply_generator_thresholds)
    
    # Generate report
    registry.generate_model_report()

if __name__ == "__main__":
    main()
