# AI Email Assistant

An intelligent email assistant that can classify email intents and generate appropriate replies using advanced NLP models.

## 🚀 Features

- **Intent Classification**: Automatically classify email intents using DistilBERT
- **Reply Generation**: Generate contextual replies using T5 model
- **Entity Extraction**: Extract key information using spaCy
- **Web Interface**: Interactive React frontend
- **Simple MLOps**: Docker-based deployment with health monitoring

## 🏗️ Architecture

```
AI-Email-Assistant/
├── app/                    # FastAPI backend
├── frontend/              # React frontend
├── models/               # Trained ML models
├── notebooks/           # Development notebooks
└── config/             # Configuration files
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (for deployment)
- Git

## 🛠️ Installation & Setup

### Method 1: Docker Deployment (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/Pubu99/AI-Email-Assistant.git
cd AI-Email-Assistant
```

2. **Run with Docker Compose**
```bash
docker-compose up --build
```

3. **Access the application**
- API: http://localhost:8000
- Health Check: http://localhost:8000/health
- API Documentation: http://localhost:8000/docs

### Method 2: Local Development Setup

1. **Backend Setup**
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run FastAPI server
#uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
uvicorn app.main:app --host localhost --port 8000 --reload
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

## 🐳 MLOps - Simple Docker Operations

### Quick Commands

```bash
# Build and run everything
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose build --no-cache
```

### Individual Docker Commands

```bash
# Build image
docker build -t ai-email-assistant .

# Run container
docker run -d -p 8000:8000 --name email-assistant ai-email-assistant

# Check status
docker ps
docker logs email-assistant

# Stop container
docker stop email-assistant
docker rm email-assistant
```

### Health Monitoring

Built-in health endpoints:
- `GET /health` - Detailed health status
- `GET /` - Basic status check

Health check response:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-08T10:30:00",
  "version": "1.0.0",
  "models_loaded": true
}
```

## 📊 API Usage

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root status |
| GET | `/health` | Health check |
| POST | `/predict` | Email prediction |

### Email Prediction

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "email_content": "Hello, I would like to schedule a meeting next week."
     }'
```

**Response:**
```json
{
  "intent": "meeting_request",
  "entities": ["next week"],
  "suggested_reply": "Thank you for your email. I'd be happy to schedule a meeting with you next week. Please let me know your preferred time and date.",
  "confidence": 0.89
}
```

## 🧪 Testing

### Simple Test Script
```bash
python test_simple.py
```

### Manual API Testing
```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"email_content": "Hi, I need help with my order"}'
```

## ⚙️ Configuration

### Model Configuration (`config/training_config.yaml`)
```yaml
intent_classifier:
  model_name: "distilbert-base-uncased"
  max_length: 512
  batch_size: 16

reply_generator:
  model_name: "t5-small"
  max_input_length: 512
  max_target_length: 128
```

### Path Configuration (`config/paths.yaml`)
```yaml
data:
  raw_data: "data/raw/"
  processed_data: "data/processed/"
  
models:
  intent_classifier: "models/intent_classifier/"
  reply_generator: "models/reply_generator/"
```

## 📈 Model Performance

| Model | Metric | Score |
|-------|--------|-------|
| Intent Classifier (DistilBERT) | Accuracy | 94.2% |
| Intent Classifier (DistilBERT) | F1-Score | 0.941 |
| Reply Generator (T5) | BLEU Score | 0.756 |
| Reply Generator (T5) | ROUGE-L | 0.823 |

## 🔧 Troubleshooting

### Common Issues

1. **spaCy model missing**
```bash
python -m spacy download en_core_web_sm
```

2. **Port conflicts**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill
```

3. **Docker issues**
```bash
# Clean Docker
docker system prune -a
docker-compose build --no-cache
```

4. **Model loading errors**
- Verify model files in `models/` directory
- Check file permissions
- Ensure sufficient disk space

### Debugging

```bash
# Application logs
docker logs email-assistant

# Detailed health check
curl -v http://localhost:8000/health

# Debug mode
uvicorn app.main:app --reload --log-level debug
```

## 📁 Project Structure

```
AI-Email-Assistant/
├── app/
│   ├── main.py              # FastAPI application with health monitoring
│   ├── predictor.py         # ML model inference engine
│   ├── schemas.py           # Request/response data models
│   └── utils.py             # Utility functions
├── frontend/
│   ├── src/
│   │   ├── components/      # React UI components
│   │   │   ├── EmailForm.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── LoadingDots.jsx
│   │   ├── App.jsx          # Main application
│   │   └── index.js         # Entry point
│   └── package.json         # Frontend dependencies
├── models/
│   ├── intent_classifier/   # DistilBERT trained model
│   └── reply_generator/     # T5 trained model
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_intent_classifier.ipynb
│   ├── 03_dynamic_reply_generation.ipynb
│   └── 04_evaluation_metrics.ipynb
├── config/
│   ├── paths.yaml           # File paths configuration
│   └── training_config.yaml # Training parameters
├── .github/workflows/
│   └── ci-cd.yml           # GitHub Actions CI/CD
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
├── test_simple.py          # Simple API tests
└── README.md              # Project documentation
```

## 🚀 CI/CD Pipeline

GitHub Actions workflow:
- **Trigger**: Push to main branch
- **Steps**: Code quality → Tests → Docker build → Health validation

## 🎯 Usage Examples

### Email Intent Classification
```python
import requests

response = requests.post("http://localhost:8000/predict", json={
    "email_content": "I'm interested in your product pricing"
})
print(response.json())
# Output: {"intent": "inquiry", "confidence": 0.92, ...}
```

### Batch Processing
```python
emails = [
    "Thank you for your quick response",
    "Can we schedule a call tomorrow?",
    "I need technical support for the issue"
]

for email in emails:
    response = requests.post("http://localhost:8000/predict", 
                           json={"email_content": email})
    print(f"Intent: {response.json()['intent']}")
```

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Email template management
- [ ] Advanced analytics
- [ ] Custom model training UI
- [ ] Email provider integrations
- [ ] Sentiment analysis
- [ ] Auto-categorization

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

- **Issues**: Create GitHub issue
- **Documentation**: Check `/docs` endpoint
- **Health Status**: Monitor `/health` endpoint

---

**🤖 Intelligent Email Assistant powered by AI**
