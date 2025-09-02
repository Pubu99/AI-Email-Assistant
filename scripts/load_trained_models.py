"""
Script to load and test pre-trained models without requiring retraining
"""
import torch
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    T5Tokenizer,
    T5ForConditionalGeneration
)
import pickle
import os

def load_intent_classifier(model_dir="../models/intent_classifier"):
    """Load the trained intent classifier model"""
    # Load tokenizer and model
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)
    model = DistilBertForSequenceClassification.from_pretrained(model_dir)
    
    # Load label encoder
    with open(os.path.join(model_dir, "label_encoder.pkl"), "rb") as f:
        label_encoder = pickle.load(f)
    
    return tokenizer, model, label_encoder

def load_reply_generator(model_dir="../models/reply_generator"):
    """Load the trained reply generator model"""
    tokenizer = T5Tokenizer.from_pretrained(model_dir)
    model = T5ForConditionalGeneration.from_pretrained(model_dir)
    return tokenizer, model

def test_models():
    """Test if models load and work correctly"""
    try:
        # Test intent classifier
        intent_tokenizer, intent_model, label_encoder = load_intent_classifier()
        print("✅ Intent classifier loaded successfully")
        
        # Test reply generator
        reply_tokenizer, reply_model = load_reply_generator()
        print("✅ Reply generator loaded successfully")
        
        # Test a sample prediction
        test_email = "Could we schedule a meeting for tomorrow?"
        
        # Predict intent
        inputs = intent_tokenizer(test_email, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = intent_model(**inputs)
        pred_id = torch.argmax(outputs.logits, dim=1).item()
        pred_intent = label_encoder.inverse_transform([pred_id])[0]
        print(f"\nTest email: {test_email}")
        print(f"Predicted intent: {pred_intent}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing pre-trained models...")
    success = test_models()
    if success:
        print("\n✨ All models loaded successfully! You can now use the trained models.")
