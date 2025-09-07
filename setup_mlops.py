#!/usr/bin/env python3
"""
MLOps Setup Script
Sets up the MLOps environment and installs necessary dependencies
"""

import subprocess
import sys
import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and handle errors"""
    logger.info(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        logger.info(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} failed: {e.stderr}")
        return False

def setup_mlops():
    """Setup MLOps environment"""
    logger.info("Setting up MLOps environment...")
    
    # Create necessary directories
    directories = [
        "mlops/reports",
        "mlops/predictions", 
        "mlops/logs",
        "mlops/artifacts",
        "deployment/staging",
        "deployment/production"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Created directory: {directory}")
    
    # Install Python dependencies
    logger.info("Installing Python dependencies...")
    success = run_command(
        "pip install -r requirements.txt",
        "Installing MLOps dependencies"
    )
    
    if not success:
        logger.error("Failed to install dependencies")
        return False
    
    # Initialize DVC
    if not Path(".dvc").exists():
        success = run_command("dvc init", "Initializing DVC")
        if not success:
            logger.warning("DVC initialization failed, continuing...")
    
    # Initialize MLflow
    success = run_command(
        "mlflow server --backend-store-uri sqlite:///mlops/mlruns.db --default-artifact-root ./mlops/artifacts --host 0.0.0.0 --port 5000 &",
        "Starting MLflow server (background)"
    )
    
    # Setup pre-commit hooks (optional)
    if Path(".git").exists():
        success = run_command("pip install pre-commit", "Installing pre-commit")
        if success:
            # Create pre-commit config
            precommit_config = """
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --ignore=E203,W503]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [tests/]
"""
            with open(".pre-commit-config.yaml", "w") as f:
                f.write(precommit_config.strip())
            
            run_command("pre-commit install", "Installing pre-commit hooks")
    
    logger.info("✓ MLOps environment setup completed!")
    
    # Print next steps
    print("""
🚀 MLOps Environment Setup Complete!

Next Steps:
1. Start MLflow UI: mlflow ui --backend-store-uri sqlite:///mlops/mlruns.db --port 5000
2. Run data preprocessing: python scripts/preprocess_data.py
3. Train models: python scripts/train_models.py
4. Set up monitoring: python scripts/run_monitoring.py --mode scheduled
5. Check drift: python scripts/check_drift.py --model intent_classifier

MLOps Features Available:
✓ Model tracking with MLflow
✓ Data version control with DVC
✓ Automated drift detection
✓ Model registry and promotion
✓ Continuous monitoring
✓ Deployment preparation
✓ CI/CD pipeline

Access MLflow UI at: http://localhost:5000
    """)

if __name__ == "__main__":
    setup_mlops()
