# Use Python image with CUDA support
FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy training code
COPY notebooks/ notebooks/
COPY app/ app/
COPY scripts/ scripts/

# Command to run training
CMD ["python", "scripts/train_models.py"]
