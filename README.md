# AI Email Assistant

A robust, production-ready AI-powered Email Categorizer and Reply Generator. Built with Python, Transformers, Docker, and MLOps best practices.

---

## 🚀 Features

- **Email Intent Classification:** Automatically categorize emails (e.g., Meeting Request, Complaint, Sales Inquiry) using transformer-based NLP models.
- **Reply Generation:** Generate context-aware, professional replies using T5 and advanced prompt engineering.
- **Entity Extraction:** Enhance responses with named entities (dates, names, topics) via spaCy.
- **Fullstack Demo:** React frontend + FastAPI backend for seamless user experience.
- **MLOps Pipeline:** Dockerized training, serving, and monitoring. MLflow for experiment tracking.

---

## ⚡ Quickstart

### 1. Prerequisites

- Docker Desktop (recommended)
- Python 3.8+ (for local dev)
- Node.js & npm (for frontend dev)

### 2. Build & Run (Docker)

```sh
docker-compose up --build
```

### 3. Local Development

1. Clone and navigate to the project:
```bash
git clone https://github.com/yourusername/AI-Email-Assistant.git
cd AI-Email-Assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be running at [http://localhost:8000](http://localhost:8000)

### Frontend Setup

1. Open a new terminal and navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

---

## 🧠 Model Training & Evaluation

- Train models in Docker or on a powerful machine, then copy `models/` to your local setup.
- Use Jupyter notebooks in `notebooks/` for data preprocessing, training, and evaluation.
- Evaluate models with `scripts/evaluate_models.py` for BLEU, ROUGE, accuracy, and more.

---

## 🛠️ MLOps & Deployment

- All services are containerized for reproducibility.
- MLflow tracks experiments and model versions.
- Monitoring scripts in `mlops/` for health and performance.

---

## 📁 Data & Privacy

- Place raw datasets in `data/raw/` (not tracked by git).
- Preprocessed data in `data/processed/`.
- Models and sensitive files are gitignored by default.

---

## 👥 Team & Contribution

- See project report for team roles and contributions.
- PRs and issues welcome!

---

## 📚 References

- Vaswani et al., "Attention is All You Need" (NeurIPS 2017)
- Wolf et al., "Transformers: State-of-the-Art NLP" (EMNLP 2020)
- [Kaggle Email Dataset](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset)
- [spaCy](https://spacy.io/)
- [MLflow](https://mlflow.org/)
- [Docker](https://docs.docker.com/)

---

## 📝 License

MIT License
