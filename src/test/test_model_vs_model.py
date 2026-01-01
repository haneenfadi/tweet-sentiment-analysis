# run the code by : python -m src.test.test_model_vs_model
import pandas as pd
from transformers import pipeline
from src.services import preprocessing
from src.utils.config import model_id_dict
# Load data
columns = ['target', 'id', 'date', 'query', 'user', 'text']
data = pd.read_csv("src/data/tweets.csv", names=columns, encoding='ISO-8859-1')


print(f"Total tweets: {len(data)}")


preprocessor = preprocessing.TweetDataProcessor()


# Test on 100 samples
sample = data.sample(100, random_state=42).copy()


# Preprocess texts BEFORE prediction
print("\nPreprocessing tweets...")
sample['text'] = sample['text'].apply(preprocessor.preprocess)
print("Preprocessing complete")


models = [
    model_id_dict["model_1"],
    model_id_dict["model_4"],
]

# Label mapping for each model
label_mappings = {

    'DunnBC22/distilbert-base-uncased-US_Airline_Twitter_Sentiment_Analysis': {
        'LABEL_0': 'negative',
        'LABEL_1': 'neutral',
        'LABEL_2': 'positive'
    }
}


print("\nComparing models on 100 tweets:\n")
print("="*70)


results = {}


for model_name in models:
    print(f"\nTesting: {model_name}")
    print("-"*70)

    sentiment = pipeline('sentiment-analysis', model=model_name)

    predictions = []
    confidences = []

    for text in sample['text']:
        try:
            result = sentiment(text[:512])
            raw_label = result[0]['label']
            # Only map if model is in label_mappings
            if model_name in label_mappings:
                mapped_label = label_mappings[model_name].get(raw_label, raw_label)
            else:
                mapped_label = raw_label.lower()

            predictions.append(mapped_label)
            confidences.append(result[0]['score'])
        except:
            predictions.append('unknown')
            confidences.append(0.0)

    # Analyze results
    unique_labels = set(predictions)
    label_dist = pd.Series(predictions).value_counts()
    avg_confidence = sum(confidences) / len(confidences)

    print(f"Labels found: {unique_labels}")
    print(f"Label distribution:\n{label_dist}")
    print(f"Average confidence: {avg_confidence:.3f}")

    results[model_name] = {
        'predictions': predictions,
        'confidences': confidences,
        'avg_confidence': avg_confidence,
        'unique_labels': len(unique_labels)
    }

    # Save to CSV
    model_short_name = model_name.split('/')[-1]
    output_df = sample.copy()
    output_df['prediction'] = predictions
    output_df['confidence'] = confidences
    output_df.to_csv(
        f"src/test/{model_short_name}_predictions.csv", index=False)
    print(f"Saved to: src/test/{model_short_name}_predictions.csv")


# Compare
print("\n" + "="*70)
print("COMPARISON")
print("="*70)


for model_name, stats in results.items():
    print(f"\n{model_name}:")
    print(f"  Average confidence: {stats['avg_confidence']:.3f}")
    print(f"  Number of classes: {stats['unique_labels']}")


# Recommendation
print("\n" + "="*70)
print("RECOMMENDATION")
print("="*70)


model_1_conf = results[model_id_dict["model_1"]]['avg_confidence']
model_4_conf = results[model_id_dict["model_4"]]['avg_confidence']


if model_1_conf > model_4_conf:
    print(
        f"✅ Use model{model_id_dict['model_1']} (confidence: {model_1_conf:.3f})")
else:
    print(f"✅ Use model{model_id_dict['model_4']} (confidence: {model_4_conf:.3f})")          