"""
Script to train models and track with MLflow
"""
import mlflow
import os
from notebooks import data_preprocessing, intent_classifier, reply_generation

def train_pipeline():
    """Run the full training pipeline"""
    try:
        mlflow.set_tracking_uri("http://mlflow:5000")
        mlflow.set_experiment("email-assistant")
        
        with mlflow.start_run(run_name="full_pipeline"):
            # Data preprocessing
            print("🔄 Starting data preprocessing...")
            data = data_preprocessing.run()
            
            # Train intent classifier
            print("🤖 Training intent classifier...")
            intent_metrics = intent_classifier.train(data)
            mlflow.log_metrics(intent_metrics)
            
            # Train reply generator
            print("✍️ Training reply generator...")
            generator_metrics = reply_generation.train(data)
            mlflow.log_metrics(generator_metrics)
            
            # Log models
            mlflow.pytorch.log_model(
                intent_classifier.model,
                "intent_classifier"
            )
            mlflow.pytorch.log_model(
                reply_generation.model,
                "reply_generator"
            )
            
            print("✅ Training completed successfully!")
            
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    train_pipeline()
