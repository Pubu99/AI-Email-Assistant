from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import EmailInput, PredictionResponse
from app.predictor import predict_all
import uvicorn
import time

app = FastAPI(
    title="AI Email Assistant",
    description="AI-powered email classification and reply generation",
    version="1.0.0"
)

# ✅ Enable CORS for frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "AI Email Assistant is running.", "version": "1.0.0"}

# Simple health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "models": {
            "intent_classifier": "loaded",
            "reply_generator": "loaded"
        }
    }

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
def get_reply(input_data: EmailInput):
    try:
        result = predict_all(input_data.email)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

# Run backend
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
