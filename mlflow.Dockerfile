# Use Python slim image
FROM python:3.8-slim

# Set working directory
WORKDIR /mlflow

# Install MLflow
RUN pip install mlflow psutil

# Expose MLflow UI port
EXPOSE 5000

# Start MLflow tracking server
CMD mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root /mlflow/artifacts \
    --host 0.0.0.0 \
    --port 5000
