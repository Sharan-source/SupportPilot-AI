import pandas as pd

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

print(df)

#Training the AI classifier model using the training data

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

X = df["ticket"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

vectorizer = TfidfVectorizer()

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

model = LogisticRegression()

model.fit(X_train_vector, y_train)

accuracy = model.score(X_test_vector, y_test)

print("Accuracy:", accuracy)