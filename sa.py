import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
df = pd.read_csv("Reviews.csv")

print("\nDataset loaded:")
print(df.head())
sia = SentimentIntensityAnalyzer()
def get_sentiment(text):
    score = sia.polarity_scores(str(text))['compound']

    if score >= 0.3:
        label = "positive"
    elif score <= -0.3:
        label = "negative"
    else:
        label = "neutral"

    return label, round(score, 3)


df["predicted_label"] = df["text"].apply(lambda x: get_sentiment(x)[0])
df["score"] = df["text"].apply(lambda x: get_sentiment(x)[1])

print("\n--- SAMPLE RESULTS ---")
print(df[["text", "label", "predicted_label", "score"]].head())

accuracy = (df["label"] == df["predicted_label"]).mean()
print("\nAccuracy:", round(accuracy, 2))

print("\nSentiment Analyzer (type 'exit' to quit)")

while True:
    text = input("\nEnter text: ")

    if text.lower() == "exit":
        break

    label, score = get_sentiment(text)

    print("Sentiment:", label)
    print("Score:", score)