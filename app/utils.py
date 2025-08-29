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
    import random
    import textblob

    persons = entities.get("PERSON", [])
    recipient = persons[0] if persons else "Unknown"  # safe fallback

    # Sentiment analysis for more dynamic replies
    blob = textblob.TextBlob(email_text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.2:
        mood = "positive"
    elif sentiment < -0.2:
        mood = "negative"
    else:
        mood = "neutral"

    entity_str = " | ".join(
        f"{k}: {', '.join(v)}" for k, v in entities.items() if v
    ) or "None"

    # Heuristic: detect urgency
    urgency_keywords = ["urgent", "asap", "immediately", "important", "priority", "soon", "deadline"]
    urgency = any(kw in email_text.lower() for kw in urgency_keywords)
    urgency_str = "urgent" if urgency else "normal"

    # Heuristic: detect formality
    formal_keywords = ["dear", "regards", "sincerely", "respectfully", "please"]
    formality = any(kw in email_text.lower() for kw in formal_keywords)
    formality_str = "formal" if formality else "informal"

    # Heuristic: extract action items (simple)
    import re
    action_items = re.findall(r"\b(?:please|kindly|can you|could you|let me know|send|provide|confirm|schedule|arrange|update|reply)\b.*?\. ", email_text, re.IGNORECASE)
    action_str = " | ".join(action_items) if action_items else "None"

    # Dynamic prompt templates by intent/category, now with urgency, formality, and action items
    category_templates = {
        "Meeting Request": [
            "You received a meeting request. Write a polite and clear reply to {recipient} about scheduling. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Formality: {formality}. Action Items: {actions}. Email: {email}",
            "Draft a response to a meeting request from {recipient}. Use a professional tone. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Action Items: {actions}. Email: {email}"
        ],
        "Job Inquiry": [
            "Respond to a job inquiry from {recipient}. Be formal and informative. Entities: {entities}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}",
            "Write a helpful reply to a job application. Entities: {entities}. Mood: {mood}. Action Items: {actions}. Email: {email}"
        ],
        "Finance": [
            "Reply to a finance-related email. Address {recipient}'s concerns about payments or invoices. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Action Items: {actions}. Email: {email}",
            "Provide a clear and concise response to a financial question. Entities: {entities}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Legal": [
            "Respond to a legal matter. Use a formal and careful tone. Entities: {entities}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}",
            "Draft a reply to a legal inquiry from {recipient}. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Action Items: {actions}. Email: {email}"
        ],
        "Appreciation": [
            "Reply to an appreciation email. Express gratitude and maintain a positive tone. Entities: {entities}. Mood: {mood}. Formality: {formality}. Email: {email}",
            "Write a warm and thankful response to {recipient}. Mood: {mood}. Email: {email}"
        ],
        "Complaint": [
            "Respond to a complaint. Be empathetic and offer solutions. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Action Items: {actions}. Email: {email}",
            "Draft a professional reply to a complaint from {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Technical Support": [
            "Reply to a technical support request. Provide clear troubleshooting steps. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Action Items: {actions}. Email: {email}",
            "Write a helpful and technical response to {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Data Request": [
            "Respond to a data request. Ensure clarity and compliance. Entities: {entities}. Mood: {mood}. Action Items: {actions}. Email: {email}",
            "Draft a reply to a request for information from {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Greeting": [
            "Reply to a greeting. Be friendly and polite. Entities: {entities}. Mood: {mood}. Formality: {formality}. Email: {email}",
            "Write a warm response to {recipient}'s greeting. Mood: {mood}. Email: {email}"
        ],
        "Farewell": [
            "Respond to a farewell message. Be courteous and wish well. Entities: {entities}. Mood: {mood}. Formality: {formality}. Email: {email}",
            "Draft a polite reply to {recipient}'s farewell. Mood: {mood}. Email: {email}"
        ],
        "Sales Inquiry": [
            "Reply to a sales inquiry. Provide product or service details. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Action Items: {actions}. Email: {email}",
            "Write a persuasive and informative response to {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Project Update": [
            "Respond to a project update. Acknowledge progress and next steps. Entities: {entities}. Mood: {mood}. Action Items: {actions}. Email: {email}",
            "Draft a reply to a project update from {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Reminder": [
            "Reply to a reminder. Confirm receipt and next actions. Entities: {entities}. Mood: {mood}. Urgency: {urgency}. Action Items: {actions}. Email: {email}",
            "Draft a response to a reminder from {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Event Planning": [
            "Respond to an event planning email. Be helpful and detail-oriented. Entities: {entities}. Mood: {mood}. Action Items: {actions}. Email: {email}",
            "Write a reply to an event planning request from {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "Personal": [
            "Reply to a personal email. Be friendly and considerate. Entities: {entities}. Mood: {mood}. Action Items: {actions}. Email: {email}",
            "Draft a warm and personal response to {recipient}. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ],
        "General Inquiry": [
            "Respond to a general inquiry. Be clear and helpful. Entities: {entities}. Mood: {mood}. Action Items: {actions}. Email: {email}",
            "Write a professional reply to {recipient}'s question. Mood: {mood}. Formality: {formality}. Action Items: {actions}. Email: {email}"
        ]
    }

    # Choose template based on intent/category
    templates = category_templates.get(intent, category_templates["General Inquiry"])
    template = random.choice(templates)
    return template.format(intent=intent, recipient=recipient, entities=entity_str, mood=mood, urgency=urgency_str, formality=formality_str, actions=action_str, email=email_text)

