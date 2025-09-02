import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.predictor import EmailPredictor
from app.utils import preprocess_text, extract_entities

def test_predictor_initialization():
    predictor = EmailPredictor()
    assert predictor is not None
    assert hasattr(predictor, 'intent_model')
    assert hasattr(predictor, 'reply_model')

def test_text_preprocessing():
    test_email = """
    Subject: Meeting Request
    From: john@example.com
    
    Hi team,
    Can we schedule a meeting tomorrow at 2 PM?
    Best regards,
    John
    """
    cleaned_text = preprocess_text(test_email)
    assert isinstance(cleaned_text, str)
    assert "Subject:" not in cleaned_text
    assert "From:" not in cleaned_text
    assert "schedule a meeting" in cleaned_text.lower()

def test_entity_extraction():
    text = "Let's meet tomorrow at 2 PM with John from Marketing"
    entities = extract_entities(text)
    assert isinstance(entities, dict)
    assert 'TIME' in entities or 'DATE' in entities
    assert 'PERSON' in entities

def test_intent_classification():
    predictor = EmailPredictor()
    test_email = "Can we schedule a meeting tomorrow at 2 PM?"
    intent = predictor.predict_intent(test_email)
    assert isinstance(intent, str)
    assert intent in predictor.valid_intents

def test_reply_generation():
    predictor = EmailPredictor()
    test_email = "Can we schedule a meeting tomorrow at 2 PM?"
    reply = predictor.generate_reply(test_email)
    assert isinstance(reply, str)
    assert len(reply) > 0
    assert "meeting" in reply.lower()  # Reply should be contextually relevant
