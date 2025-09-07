#!/usr/bin/env python3
"""
Deployment Preparation Script
Prepares models and configurations for deployment to staging/production
"""

import os
import json
import yaml
import shutil
import logging
from datetime import datetime
from pathlib import Path
import argparse
import subprocess
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mlops.model_registry import ModelRegistry

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentPreparator:
    def __init__(self, config_path="config/mlops_config.yaml"):
        """Initialize deployment preparator"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['mlops']
        
        self.model_registry = ModelRegistry()
        self.deployment_dir = Path("deployment")
        
    def validate_models(self) -> bool:
        """Validate models before deployment"""
        logger.info("Validating models for deployment...")
        
        validation_results = {}
        
        for model_name in ['intent_classifier', 'reply_generator']:
            # Get production model info
            model_info = self.model_registry.get_model_info(model_name, 'Production')
            
            if not model_info:
                logger.error(f"No production model found for {model_name}")
                validation_results[model_name] = False
                continue
            
            # Check minimum performance thresholds
            thresholds = self.config['model_validation']
            meets_requirements = True
            
            if 'accuracy' in model_info['metrics']:
                if model_info['metrics']['accuracy'] < thresholds.get('minimum_accuracy', 0.75):
                    logger.error(f"{model_name} accuracy below threshold: "
                               f"{model_info['metrics']['accuracy']}")
                    meets_requirements = False
            
            # Check model size (optional)
            # Check inference time (optional)
            
            validation_results[model_name] = meets_requirements
            
            if meets_requirements:
                logger.info(f"✓ {model_name} validation passed")
            else:
                logger.error(f"✗ {model_name} validation failed")
        
        return all(validation_results.values())
    
    def prepare_model_artifacts(self, target_env: str = "production") -> str:
        """Prepare model artifacts for deployment"""
        logger.info(f"Preparing model artifacts for {target_env}...")
        
        # Create deployment directory
        env_dir = self.deployment_dir / target_env
        env_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy production models
        models_dir = env_dir / "models"
        models_dir.mkdir(exist_ok=True)
        
        deployment_manifest = {
            'deployment_timestamp': datetime.now().isoformat(),
            'target_environment': target_env,
            'models': {}
        }
        
        for model_name in ['intent_classifier', 'reply_generator']:
            model_info = self.model_registry.get_model_info(model_name, 'Production')
            
            if model_info:
                # Copy model files
                source_model_dir = Path(f"models/{model_name}")
                target_model_dir = models_dir / model_name
                
                if source_model_dir.exists():
                    shutil.copytree(source_model_dir, target_model_dir, dirs_exist_ok=True)
                    logger.info(f"Copied {model_name} to deployment directory")
                    
                    deployment_manifest['models'][model_name] = {
                        'version': model_info['version'],
                        'metrics': model_info['metrics'],
                        'model_path': str(target_model_dir)
                    }
                else:
                    logger.warning(f"Model directory not found: {source_model_dir}")
        
        # Save deployment manifest
        manifest_path = env_dir / "deployment_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(deployment_manifest, f, indent=2, default=str)
        
        logger.info(f"Deployment manifest saved to {manifest_path}")
        return str(env_dir)
    
    def generate_docker_config(self, target_env: str = "production") -> str:
        """Generate Docker configuration for deployment"""
        logger.info(f"Generating Docker configuration for {target_env}...")
        
        env_dir = self.deployment_dir / target_env
        
        # Production Dockerfile
        dockerfile_content = f"""
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY models/ ./models/
COPY config/ ./config/

# Copy deployment-specific files
COPY deployment/{target_env}/models/ ./models/

# Set environment variables
ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/models
ENV ENVIRONMENT={target_env}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        
        dockerfile_path = env_dir / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content.strip())
        
        # Docker Compose for production
        docker_compose_content = f"""
version: "3.8"

services:
  email-assistant-api:
    build:
      context: ../..
      dockerfile: deployment/{target_env}/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT={target_env}
      - MODEL_PATH=/app/models
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    
  mlflow:
    image: python:3.11-slim
    command: >
      bash -c "pip install mlflow[extras] &&
               mlflow server --host 0.0.0.0 --port 5000 
               --backend-store-uri sqlite:///mlflow.db 
               --default-artifact-root ./artifacts"
    ports:
      - "5000:5000"
    volumes:
      - mlflow_data:/mlflow
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - email-assistant-api
    restart: unless-stopped

volumes:
  mlflow_data:
"""
        
        compose_path = env_dir / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            f.write(docker_compose_content.strip())
        
        logger.info(f"Docker configuration saved to {env_dir}")
        return str(dockerfile_path)
    
    def generate_k8s_manifests(self, target_env: str = "production") -> str:
        """Generate Kubernetes manifests for deployment"""
        logger.info(f"Generating Kubernetes manifests for {target_env}...")
        
        env_dir = self.deployment_dir / target_env / "k8s"
        env_dir.mkdir(parents=True, exist_ok=True)
        
        # Deployment manifest
        deployment_manifest = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: email-assistant-{target_env}
  labels:
    app: email-assistant
    environment: {target_env}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: email-assistant
      environment: {target_env}
  template:
    metadata:
      labels:
        app: email-assistant
        environment: {target_env}
    spec:
      containers:
      - name: email-assistant
        image: email-assistant:{target_env}
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "{target_env}"
        - name: MODEL_PATH
          value: "/app/models"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: email-assistant-service-{target_env}
spec:
  selector:
    app: email-assistant
    environment: {target_env}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: email-assistant-ingress-{target_env}
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api-{target_env}.yourdomain.com
    secretName: email-assistant-tls-{target_env}
  rules:
  - host: api-{target_env}.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: email-assistant-service-{target_env}
            port:
              number: 80
"""
        
        manifest_path = env_dir / "deployment.yaml"
        with open(manifest_path, 'w') as f:
            f.write(deployment_manifest.strip())
        
        logger.info(f"Kubernetes manifests saved to {env_dir}")
        return str(manifest_path)
    
    def run_tests(self, target_env: str = "production") -> bool:
        """Run deployment tests"""
        logger.info(f"Running deployment tests for {target_env}...")
        
        try:
            # Run unit tests
            result = subprocess.run([
                'python', '-m', 'pytest', 'tests/', '-v'
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Unit tests failed: {result.stderr}")
                return False
            
            # Run integration tests (if they exist)
            integration_tests = Path("tests/integration")
            if integration_tests.exists():
                result = subprocess.run([
                    'python', '-m', 'pytest', 'tests/integration/', '-v'
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    logger.error(f"Integration tests failed: {result.stderr}")
                    return False
            
            logger.info("✓ All tests passed")
            return True
            
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return False
    
    def create_deployment_package(self, target_env: str = "production") -> str:
        """Create complete deployment package"""
        logger.info(f"Creating deployment package for {target_env}...")
        
        # Validate models
        if not self.validate_models():
            raise ValueError("Model validation failed")
        
        # Run tests
        if not self.run_tests(target_env):
            raise ValueError("Tests failed")
        
        # Prepare artifacts
        deployment_path = self.prepare_model_artifacts(target_env)
        
        # Generate configurations
        self.generate_docker_config(target_env)
        self.generate_k8s_manifests(target_env)
        
        # Create deployment summary
        summary = {
            'deployment_id': f"{target_env}_{datetime.now().strftime('%Y%m%d_%H%M')}",
            'target_environment': target_env,
            'deployment_path': deployment_path,
            'created_at': datetime.now().isoformat(),
            'models_included': ['intent_classifier', 'reply_generator'],
            'validation_status': 'passed',
            'test_status': 'passed'
        }
        
        summary_path = Path(deployment_path) / "deployment_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"✓ Deployment package created successfully at {deployment_path}")
        logger.info(f"Deployment ID: {summary['deployment_id']}")
        
        return deployment_path

def main():
    parser = argparse.ArgumentParser(description="Prepare deployment package")
    parser.add_argument("--environment", choices=['staging', 'production'], 
                       default='staging', help="Target deployment environment")
    parser.add_argument("--validate-only", action='store_true',
                       help="Only validate models without creating package")
    
    args = parser.parse_args()
    
    preparator = DeploymentPreparator()
    
    if args.validate_only:
        if preparator.validate_models():
            logger.info("✓ Model validation passed")
        else:
            logger.error("✗ Model validation failed")
            sys.exit(1)
    else:
        try:
            deployment_path = preparator.create_deployment_package(args.environment)
            logger.info(f"Deployment package ready: {deployment_path}")
        except Exception as e:
            logger.error(f"Deployment preparation failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()