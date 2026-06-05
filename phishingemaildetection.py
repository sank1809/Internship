import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix

# Sample dataset (No CSV file required)
data = pd.DataFrame({
    "text": [
        "Click here to claim your free prize now",
        "Your account has been suspended verify immediately",
        "Congratulations you won a lottery",
        "Update your bank details urgently",
        "Meeting scheduled for tomorrow at 10 AM",
        "Please find the attached project report",
        "Lunch with team today",
        "Project submission deadline extended"
    ],
    "label": [
        "phishing",
        "phishing",
        "phishing",
        "phishing",
        "safe",
        "safe",
        "safe",
        "safe"
    ]
})

# Features and labels
X = data["text"]
y = data["label"]

# Convert text to numerical features
vectorizer = TfidfVectorizer()
X_features = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_features, y, test_size=0.25, random_state=42
)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

# Accuracy
print("Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")

# Confusion Matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# User input for prediction
while True:
    email = input("\nEnter email text (or type 'exit' to quit): ")

    if email.lower() == "exit":
        break

    email_vector = vectorizer.transform([email])
    result = model.predict(email_vector)

    print("Prediction:", result[0].upper())
