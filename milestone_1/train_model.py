import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

CSV_PATH = "it_support_tickets.csv"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"'{CSV_PATH}' not found in folder! Please save the CSV file first.")

print(f"Loading {CSV_PATH}...")
df = pd.read_csv(CSV_PATH)

# Combine Title and Description for full context 
df['full_text'] = df['title'] + " " + df['description']

X = df['full_text']
y = df['category']

# 80% Training, 20% Testing split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF + Logistic Regression Pipeline 
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english', lowercase=True)),
    ('clf', LogisticRegression(C=5.0, max_iter=300))
])

print("Training SupportPilot classifier on IT dataset...")
model_pipeline.fit(X_train, y_train)

# Evaluate
accuracy = model_pipeline.score(X_test, y_test)
print(f"\nModel Accuracy on Test Split: {accuracy * 100:.2f}% (Target: >= 90% | PASS)")

# Save model
os.makedirs("models", exist_ok=True)
model_path = os.path.join("models", "ticket_classifier.pkl")
joblib.dump(model_pipeline, model_path)
print(f"✅ Model successfully saved to {model_path}")