# AI-Powered Email Categorizer & Reply Generator

An AI-powered email assistant that automatically classifies email intents and generates contextual replies using advanced transformer models.

## Features

### Core AI Capabilities

- **Intent Classification**: Automatically categorizes emails (inquiry, complaint, request, feedback)
- **Dynamic Reply Generation**: Generates contextual responses using transformer models
- **Multi-Model Architecture**: DistilBERT for classification + T5 for text generation
- **Real-time API**: FastAPI-based REST API for seamless integration

## Architecture

```
├── Frontend (React)
├── API Layer (FastAPI)
└── ML Models
    ├── Intent Classifier (DistilBERT)
    └── Reply Generator (T5)
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+ (for frontend)

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

### 3. Start the Application

```bash
# Start API server
uvicorn app.main:app --host localhost --port 8000 --reload

# Start frontend (in separate terminal)
cd frontend
npm install
npm start
```

## API Documentation

- Interactive API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000 (User interface)

## Project Structure

```
AI-Email-Assistant/
├── app/                       # FastAPI application
│   ├── main.py                # API entry point
│   ├── predictor.py          # Model inference logic
│   ├── schemas.py            # Pydantic models
│   └── utils.py              # Utility functions
├── frontend/                 # React frontend
│   ├── src/components/       # React components
│   └── public/               # Static assets
├── models/                   # Trained models
│   ├── intent_classifier/    # DistilBERT model
│   └── reply_generator/      # T5 model
├── config/                   # Configuration files
│   ├── training_config.yaml  # Training parameters
│   └── paths.yaml           # Data paths
├── notebooks/                # Jupyter notebooks
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Configuration

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

## Testing

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
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/Pubu99/AI-Email-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Pubu99/AI-Email-Assistant/discussions)
