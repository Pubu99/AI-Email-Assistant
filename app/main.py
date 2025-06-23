from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import EmailInput, PredictionResponse
from app.predictor import predict_all
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
    result = predict_all(input_data.email)
    print("DEBUG:", result)  # 👈 Add this
    return PredictionResponse(**result)


# Run backend
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
