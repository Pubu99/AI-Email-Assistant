import torch
import os
import pickle
from transformers import (
    DistilBertTokenizerFast, DistilBertForSequenceClassification,
    T5Tokenizer, T5ForConditionalGeneration
)
from app.utils import extract_entities, build_prompt

# Device config
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Load models and tokenizers ===

# Intent classifier
intent_model_dir = "models/intent_classifier"
intent_tokenizer = DistilBertTokenizerFast.from_pretrained(intent_model_dir)
intent_model = DistilBertForSequenceClassification.from_pretrained(intent_model_dir).to(device)
with open(os.path.join(intent_model_dir, "label_encoder.pkl"), "rb") as f:
    label_encoder = pickle.load(f)

# Reply generator
reply_model_dir = "models/reply_generator"
reply_tokenizer = T5Tokenizer.from_pretrained(reply_model_dir)
reply_model = T5ForConditionalGeneration.from_pretrained(reply_model_dir).to(device)

# === Inference logic ===
def predict_all(email_text: str) -> dict:
    # Predict intent
    inputs = intent_tokenizer(email_text, truncation=True, padding=True, return_tensors="pt", max_length=512).to(device)
    with torch.no_grad():
        logits = intent_model(**inputs).logits
    pred_id = torch.argmax(logits, dim=1).item()
    intent_label = label_encoder.inverse_transform([pred_id])[0]

    # Extract entities
    entities = extract_entities(email_text)

    # Build prompt and generate reply
    prompt = build_prompt(email_text, intent_label, entities)
    t5_inputs = reply_tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = reply_model.generate(**t5_inputs, max_length=128)
    reply_text = reply_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "intent": intent_label,
        "reply": reply_text
    }
