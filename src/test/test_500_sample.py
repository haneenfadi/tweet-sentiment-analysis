# run the code by : python -m src.test.500_sample
from src.services import preprocessing, tweets_analysis
import pandas as pd


columns = ['target', 'id', 'date', 'query', 'user', 'text']
data = pd.read_csv("src/data/tweets.csv", names=columns, encoding='ISO-8859-1')

print(f"Total tweets: {len(data)}")


sample = data.sample(n=500, random_state=42)

print("Preprocessing and getting predictions...")

# predictions
preprocessor = preprocessing.TweetDataProcessor()
sentiment_model = tweets_analysis.SentimentModel()

results = []
for idx, row in sample.iterrows():
    cleaned = preprocessor.preprocess(row['text'])
    prediction = sentiment_model.predict_sentiment(cleaned)

    results.append({
        'text': row['text'],
        'model_prediction': prediction,
        # 'my_label': ''  if you want to add your own labels later for review purposes 
    })

df = pd.DataFrame(results)
df.to_csv('src/test/tweets_model(4)_test.csv',
          index=False, encoding='ISO-8859-1')

print(f"\n✅{len(results)} 'tweets_model(4)_test.csv'")

