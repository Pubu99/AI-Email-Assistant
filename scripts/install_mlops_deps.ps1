echo "Installing additional dependencies for MLOps and advanced features..."

pip install mlflow>=1.17.0 wandb>=0.10.31
pip install pytest>=6.2.4 pytest-cov>=2.12.0
pip install dvc>=2.1.0 black>=21.5b1 flake8>=3.9.2 isort>=5.8.0
pip install bert-score>=0.3.8 sentence-transformers>=2.0.0
pip install seaborn>=0.11.1

echo "Dependencies installed successfully!"
