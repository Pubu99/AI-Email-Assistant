import spacy

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    return {
        "PERSON": list(set(ent.text for ent in doc.ents if ent.label_ == "PERSON")),
        "DATE": list(set(ent.text for ent in doc.ents if ent.label_ == "DATE")),
        "ORG": list(set(ent.text for ent in doc.ents if ent.label_ == "ORG")),
        "GPE": list(set(ent.text for ent in doc.ents if ent.label_ == "GPE"))
    }

def build_prompt(email_text: str, intent: str, entities: dict) -> str:
    persons = entities.get("PERSON", [])
    recipient = persons[0] if persons else "Unknown"  # safe fallback

    entity_str = " | ".join(
        f"{k}: {', '.join(v)}" for k, v in entities.items() if v
    ) or "None"

    return f"Intent: {intent} | RecipientName: {recipient} | Entities: {entity_str} | Email: {email_text}"

