from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import EmailInput, PredictionResponse
from predictor import predict_all
import uvicorn

app = FastAPI(title="AI Email Assistant")

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
    return {"message": "AI Email Assistant is running."}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
def get_reply(input_data: EmailInput):
    return predict_all(input_data.email)

# Run backend
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
