import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Training Data 

data = {
    "ticket": [
        "WiFi is not working",
        "Internet connection is very slow",
        "VPN is not connecting",
        "Unable to access company VPN",
        "I forgot my password",
        "Please reset my password",
        "Install Microsoft Office",
        "Application installation required",
        "Laptop keyboard is not working",
        "Monitor display is not working"
    ],
    "category": [
        "Network",
        "Network",
        "VPN",
        "VPN",
        "Password",
        "Password",
        "Software",
        "Software",
        "Hardware",
        "Hardware"
    ]
}

df = pd.DataFrame(data)

# ==========================================
# 2. Train Model (TF-IDF + Logistic Regression)
# ==========================================
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(df["ticket"])
y_train = df["category"]

model = LogisticRegression()
model.fit(X_train, y_train)

# 3. Severity Prediction 

def predict_severity(ticket):
    text = ticket.lower()
    
    critical_words = [
        "server down",
        "entire company",
        "production down",
        "security breach"
    ]
    
    high_words = [
        "urgent",
        "cannot work",
        "business stopped",
        "client meeting",
        "vpn not working"
    ]
    
    medium_words = [
        "slow",
        "error",
        "problem",
        "issue"
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

# 4.Priority Calculation 

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

# ==========================================
# 5. Complete Milestone 1 Demo: process_ticket()
# ==========================================
def process_ticket(ticket, business_impact="Normal"):
    # 1. Category Classification
    ticket_vector = vectorizer.transform([ticket])
    category = model.predict(ticket_vector)[0]
    
    # 2. Severity Prediction
    severity = predict_severity(ticket)
    
    # 3. Priority Calculation
    # If the user mentions 'client meeting' or 'urgent', bump business impact to High
    if "client meeting" in ticket.lower() or "urgent" in ticket.lower():
        business_impact = "High"
        
    priority = calculate_priority(severity, business_impact)
    
    return category, severity, priority

# ==========================================
# 6. Test with Sample Ticket 
# ==========================================
if __name__ == "__main__":
    test_ticket = """URGENT: VPN is not connecting.
I cannot work and I have an important client meeting."""

    category, severity, priority = process_ticket(test_ticket)

    print("=" * 45)
    print("SUPPORTPILOT - MILESTONE 1 CLASSIFICATION")
    print("=" * 45)
    print("Ticket:\n", test_ticket.strip())
    print("-" * 45)
    print("Predicted Category :", category)
    print("Severity           :", severity)
    print("Priority           :", priority)
    print("=" * 45)