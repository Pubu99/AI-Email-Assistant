from pydantic import BaseModel

class EmailInput(BaseModel):
    email: str

class PredictionResponse(BaseModel):
    intent: str
    reply: str
