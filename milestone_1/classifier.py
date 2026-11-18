import os
import joblib
import numpy as np

MODEL_PATH = os.path.join("models", "ticket_classifier.pkl")

def get_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    raise FileNotFoundError("Run train_model.py first to create models/ticket_classifier.pkl")

# Exact keyword severity engine from 
def predict_severity(ticket):
    text = ticket.lower()
    
    # Critical keywords 
    critical_words = [
        "server down", "entire company", "production down", 
        "security breach", "critical outage", "unauthorized access", 
        "database cluster", "backup system failure"
    ]
    # High keywords 
    high_words = [
        "urgent", "cannot work", "business stopped", "client meeting", 
        "vpn not working", "vpn is not connecting", "blue screen", 
        "computer will not start", "timeout"
    ]
    # Medium keywords 
    medium_words = [
        "slow", "error", "problem", "issue", "disconnected", 
        "not working", "paper jam", "draining", "frozen", "crashing"
    ]

    for word in critical_words:
        if word in text:
            return "Critical"
    for word in high_words:
        if word in text:
            return "High"
    for word in medium_words:
        if word in text:
            return "Medium"
    return "Low"

# Priority calculation matrix 
def calculate_priority(severity, business_impact="Normal"):
    if severity == "Critical" and business_impact == "High":
        return "P1"
    elif severity == "High" and business_impact == "High":
        return "P1"
    elif severity == "Critical":
        return "P1"
    elif severity == "High":
        return "P2"
    elif severity == "Medium":
        return "P3"
    else:
        return "P4"

# Combined master function 
def process_ticket(ticket):
    model = get_model()

    # 1. Classification & Confidence
    predicted_category = model.predict([ticket])[0]
    probabilities = model.predict_proba([ticket])[0]
    confidence = float(np.max(probabilities))

    # 2. Severity
    severity = predict_severity(ticket)

    # 3. Priority Calculation
    impact = "High" if ("client meeting" in ticket.lower() or "urgent" in ticket.lower() or "entire company" in ticket.lower()) else "Normal"
    priority = calculate_priority(severity, impact)

    return predicted_category, severity, priority, confidence