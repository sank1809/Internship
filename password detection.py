import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix

# Sample dataset
data = {
    "email": [
        "Win money now",
        "Your account is blocked click here",
        "Meeting at 10 AM",
        "Project submission tomorrow",
        "Claim free reward now",
        "Important bank update verify now"
    ],
    "label": [
        "phishing",
        "phishing",
        "safe",
        "safe",
        "phishing",
        "phishing"
    ]
}

df = pd.DataFrame(data)

# Convert text into numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["email"])

y = df["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# Confusion Matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Test custom email
msg = input("\nEnter Email Message: ")

msg_data = vectorizer.transform([msg])

prediction = model.predict(msg_data)

print("Prediction:", prediction[0])
