# 🤖 AI Email Assistant with MLOps

An enterprise-grade AI-powered email assistant that automatically classifies email intents and generates contextual replies. Built with comprehensive MLOps practices including experiment tracking, model monitoring, drift detection, and automated deployment pipelines.

## 🌟 Features

### Core AI Capabilities

- **Intent Classification**: Automatically categorizes emails (inquiry, complaint, request, feedback)
- **Dynamic Reply Generation**: Generates contextual responses using transformer models
- **Multi-Model Architecture**: DistilBERT for classification + T5 for text generation
- **Real-time API**: FastAPI-based REST API for seamless integration

### MLOps & Production Ready

- **🔬 Experiment Tracking**: MLflow integration for comprehensive experiment management
- **📊 Model Monitoring**: Real-time performance monitoring and drift detection
- **🔄 CI/CD Pipeline**: Automated testing, validation, and deployment
- **📦 Model Registry**: Centralized model versioning and promotion
- **🚀 Deployment**: Docker, Kubernetes, and cloud-ready configurations
- **📈 Data Pipeline**: DVC-managed reproducible data processing
- **⚠️ Alert System**: Automated notifications for model degradation

## 🏗️ Architecture

```
├── 📱 Frontend (React)
├── 🔌 API Layer (FastAPI)
├── 🧠 ML Models
│   ├── Intent Classifier (DistilBERT)
│   └── Reply Generator (T5)
├── 📊 MLOps Infrastructure
│   ├── MLflow (Experiment Tracking)
│   ├── DVC (Data Versioning)
│   ├── Model Registry
│   └── Monitoring System
└── 🚀 Deployment
    ├── Docker Containers
    ├── Kubernetes Manifests
    └── CI/CD Pipeline
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+ (for frontend)
- Docker (optional, for containerized deployment)
- Git with LFS support

### 1. Clone Repository

```bash
git clone https://github.com/Pubu99/AI-Email-Assistant.git
cd AI-Email-Assistant
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize MLOps Environment

```bash
# Run MLOps setup script
python setup_mlops.py

# Initialize DVC
dvc init

# Create necessary directories
mkdir mlops\reports mlops\predictions mlops\logs mlops\artifacts
mkdir deployment\staging deployment\production
```

### 4. Start MLflow Tracking Server

```bash
# Start MLflow in a separate terminal
mlflow server --backend-store-uri sqlite:///mlops/mlruns.db --default-artifact-root ./mlops/artifacts --host 0.0.0.0 --port 5000
```

### 5. Run Data Pipeline

```bash
# Execute complete DVC pipeline
dvc repro

# Or run individual stages
dvc repro data_preprocessing
dvc repro train_intent_classifier
dvc repro train_reply_generator
```

### 6. Start the Application

```bash
# Start API server
uvicorn app.main:app --host localhost --port 8000 --reload

# Start frontend (in separate terminal)
cd frontend
npm install
npm start
```

## 📊 MLOps Workflow

### Experiment Tracking

```bash
# Train models with automatic MLflow logging
python scripts/train_models.py --model intent_classifier
python scripts/train_models.py --model reply_generator

# View experiments at http://localhost:5000
```

### Model Registry Management

```bash
# Auto-promote models based on performance
python -c "
from mlops.model_registry import ModelRegistry
registry = ModelRegistry()
thresholds = {'accuracy': 0.85, 'f1_score': 0.80}
registry.auto_promote_model('intent_classifier', thresholds)
"

# Manual model promotion
python -c "
from mlops.model_registry import ModelRegistry
registry = ModelRegistry()
registry.promote_model('intent_classifier', '1', 'Production')
"
```

### Monitoring & Drift Detection

```bash
# Run monitoring once
python scripts/run_monitoring.py --mode once

# Continuous monitoring (background)
python scripts/run_monitoring.py --mode scheduled

# Check for drift
python scripts/check_drift.py --model intent_classifier
python scripts/check_drift.py --model reply_generator
```

### Model Evaluation

```bash
# Evaluate all models
python scripts/evaluate_models.py

# Validate models for deployment
python scripts/validate_models.py

# Generate monitoring reports
python scripts/generate_monitoring_report.py
```

## 🐳 Docker Deployment

### Development

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

### Production Deployment

```bash
# Prepare deployment package
python scripts/prepare_deployment.py --environment production

# Deploy with production configuration
cd deployment/production
docker-compose up -d
```

## ☸️ Kubernetes Deployment

```bash
# Generate Kubernetes manifests
python scripts/prepare_deployment.py --environment production

# Apply manifests
kubectl apply -f deployment/production/k8s/

# Check deployment status
kubectl get pods -l app=email-assistant
```

## 🔄 CI/CD Pipeline

The project includes GitHub Actions workflow (`.github/workflows/mlops_pipeline.yml`) that automatically:

### On Push to Main:

1. **Test**: Run unit and integration tests
2. **Validate**: Data and model validation
3. **Train**: Execute DVC pipeline
4. **Monitor**: Check for drift and performance issues
5. **Deploy**: Automated deployment to staging

### Daily Scheduled:

1. **Monitor**: Performance and drift monitoring
2. **Report**: Generate comprehensive reports
3. **Alert**: Notify on issues

## 📈 Monitoring Dashboard

### Access Points

- **MLflow UI**: http://localhost:5000 (Experiment tracking)
- **API Documentation**: http://localhost:8000/docs (Interactive API docs)
- **Health Check**: http://localhost:8000/health (System status)
- **Frontend**: http://localhost:3000 (User interface)

### Key Metrics Monitored

- **Model Performance**: Accuracy, F1-score, BLEU score
- **Data Quality**: Schema validation, statistical properties
- **System Health**: API response time, error rates
- **Drift Detection**: Data distribution changes, model degradation

## 📁 Project Structure

```
AI-Email-Assistant/
├── 📁 app/                     # FastAPI application
│   ├── main.py                 # API entry point
│   ├── predictor.py           # Model inference logic
│   ├── schemas.py             # Pydantic models
│   └── utils.py               # Utility functions
├── 📁 frontend/               # React frontend
│   ├── src/components/        # React components
│   └── public/                # Static assets
├── 📁 models/                 # Trained models
│   ├── intent_classifier/     # DistilBERT model
│   └── reply_generator/       # T5 model
├── 📁 mlops/                  # MLOps infrastructure
│   ├── model_monitor.py       # Model monitoring
│   ├── model_registry.py      # Model registry management
│   ├── reports/               # Generated reports
│   ├── predictions/           # Prediction logs
│   └── artifacts/             # MLflow artifacts
├── 📁 scripts/                # MLOps scripts
│   ├── train_models.py        # Model training
│   ├── evaluate_models.py     # Model evaluation
│   ├── check_drift.py         # Drift detection
│   ├── run_monitoring.py      # Monitoring orchestrator
│   └── prepare_deployment.py  # Deployment preparation
├── 📁 config/                 # Configuration files
│   ├── training_config.yaml   # Training parameters
│   ├── paths.yaml            # Data paths
│   └── mlops_config.yaml     # MLOps settings
├── 📁 data/                   # Dataset
│   ├── raw/                   # Original data
│   └── processed/             # Cleaned data
├── 📁 notebooks/              # Jupyter notebooks
├── 📁 tests/                  # Test files
├── 📁 deployment/             # Deployment configurations
│   ├── staging/               # Staging environment
│   └── production/            # Production environment
├── 🐳 docker-compose.yml      # Docker orchestration
├── 🔧 dvc.yaml               # DVC pipeline definition
├── 📄 requirements.txt        # Python dependencies
└── 🚀 setup_mlops.py         # MLOps setup script
```

## 🔧 Configuration

### MLOps Configuration (`config/mlops_config.yaml`)

```yaml
mlops:
  mlflow:
    tracking_uri: "sqlite:///mlops/mlruns.db"
    experiment_name: "email_assistant"

  drift_detection:
    enabled: true
    data_drift_threshold: 0.05
    model_drift_threshold: 0.1
    monitoring_window_days: 7

  model_registry:
    auto_promotion: true
    performance_thresholds:
      intent_classifier:
        accuracy: 0.85
        f1_score: 0.80
```

### Training Configuration (`config/training_config.yaml`)

```yaml
training:
  intent_classifier:
    model_name: "distilbert-base-uncased"
    max_length: 128
    batch_size: 16
    learning_rate: 2e-5
    epochs: 3

  reply_generator:
    model_name: "t5-small"
    max_length: 256
    batch_size: 8
    learning_rate: 3e-4
    epochs: 5
```

## 🧪 Testing

### Run All Tests

```bash
# Unit tests
pytest tests/ -v

# Integration tests
pytest tests/integration/ -v

# Coverage report
pytest tests/ --cov=app --cov-report=html
```

### Model-Specific Tests

```bash
# Test model inference
python -m pytest tests/test_models.py

# Test API endpoints
python -m pytest tests/test_api.py

# Test MLOps components
python -m pytest tests/test_mlops.py
```

## 🔍 Troubleshooting

### Common Issues

1. **MLflow Server Not Starting**

   ```bash
   # Check if port 5000 is available
   netstat -an | findstr :5000

   # Use different port
   mlflow server --port 5001 --backend-store-uri sqlite:///mlops/mlruns.db
   ```

2. **DVC Pipeline Fails**

   ```bash
   # Check DVC status
   dvc status

   # Force reproduce
   dvc repro --force
   ```

3. **Model Loading Issues**

   ```bash
   # Verify model files
   ls models/intent_classifier/

   # Check model registry
   python -c "from mlops.model_registry import ModelRegistry; print(ModelRegistry().list_models())"
   ```

### Debug Commands

```bash
# Check system health
curl http://localhost:8000/health

# View recent logs
tail -f mlops/logs/application.log

# Check MLflow experiments
mlflow experiments list

# Monitor disk usage
dvc cache dir
```

## 📚 Documentation

### API Documentation

- Interactive API docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

### Model Documentation

- Model cards available in `models/*/README.md`
- Training metrics in MLflow UI
- Performance reports in `mlops/reports/`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Workflow

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install
pre-commit run --all-files

# Run tests before committing
pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♀️ Support

- **Issues**: [GitHub Issues](https://github.com/Pubu99/AI-Email-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Pubu99/AI-Email-Assistant/discussions)
- **Documentation**: Check the `docs/` folder for detailed guides

## 🎯 Roadmap

- [ ] **Advanced Monitoring**: Implement Prometheus + Grafana
- [ ] **A/B Testing**: Multi-model comparison framework
- [ ] **Edge Deployment**: ONNX model optimization
- [ ] **Advanced NLP**: Support for multiple languages
- [ ] **Integration**: Slack, Discord, Teams connectors
- [ ] **Analytics**: Advanced email analytics dashboard

---
