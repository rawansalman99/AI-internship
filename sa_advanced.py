import pandas as pd
import re
import nltk
import joblib

from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

nltk.download('stopwords')

data = pd.read_csv("Reviews.csv")

print("\nDataset Preview:")
print(data.head())

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)

data["clean_text"] = data["text"].apply(clean_text)

vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))

X = vectorizer.fit_transform(data["clean_text"])
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=300)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nModel Evaluation:")
print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("F1 Score:", round(f1_score(y_test, y_pred, average="weighted"), 3))

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

def predict_sentiment(text):
    cleaned = clean_text(text)

    # If empty after cleaning → neutral
    if cleaned.strip() == "":
        return "neutral"

    vector = vectorizer.transform([cleaned])

    # If no known words → neutral
    if vector.nnz == 0:
        return "neutral"

    return model.predict(vector)[0]

positive_words = {"love", "great", "amazing", "good", "happy", "excellent", "nice"}
negative_words = {"hate", "bad", "terrible", "awful", "sad", "worst", "exhausted"}

def fallback_sentiment(text):
    words = text.lower().split()

    for w in words:
        if w in positive_words:
            return "positive"
        if w in negative_words:
            return "negative"

    return None

def final_predict(text):
    fallback = fallback_sentiment(text)

    if fallback is not None:
        return fallback

    return predict_sentiment(text)

print("\nSmart Sentiment Analyzer (type 'exit' to quit)")

while True:
    user_input = input("\nEnter text: ")

    if user_input.lower() == "exit":
        break

    result = final_predict(user_input)

    print("Predicted Sentiment:", result)