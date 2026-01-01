# Sampled 100 tweets for manual evaluation, run the code by : python -m src.test.evaluate
# to Compare with your manual labels, run the code by : python -m src.test.evaluate manual
from src.services import  preprocessing, tweets_analysis
import pandas as pd
import json
from sklearn.metrics import classification_report, confusion_matrix
import sys

class ManualEvaluation:
    def __init__(self, sample_size=100):
        columns = ['target', 'id', 'date', 'query', 'user', 'text']
        self.data = pd.read_csv("src/data/tweets.csv",
                                names=columns, encoding='ISO-8859-1')

        self.sample = self.data.sample(n=sample_size, random_state=42)
        print(f"Sampled {len(self.sample)} tweets for manual evaluation")

    def predict_and_save_for_manual_review(self):
        print("Preprocessing and predicting...")
        preprocessor = preprocessing.TweetDataProcessor()
        sentiment_model = tweets_analysis.SentimentModel()

        results = []
        for idx, row in self.sample.iterrows():
            cleaned = preprocessor.preprocess(row['text'])
            prediction = sentiment_model.predict_sentiment(cleaned)

            results.append({
                'id': idx,
                'text': row['text'],
                'model_prediction': prediction,
                'manual_label': '',
                'notes': ''
            })

        # Save to CSV for manual review
        df = pd.DataFrame(results)
        df.to_csv('src/test/manual_evaluation.csv', index=False, encoding='utf-8-sig')

        print("\nSaved to 'manual_evaluation.csv'")
        print(" Review each tweet and fill 'manual_label' column with:")
        print("   - positive")
        print("   - negative")
        print("   - neutral")
        return df

    def calculate_accuracy_from_manual_labels(self):
        """Compare model predictions with your manual labels"""

        df = pd.read_csv('src/test/manual_evaluation.csv', encoding='utf-8-sig')
        df = df[df['manual_label'].notna() & (df['manual_label'] != '')]

        if len(df) == 0:
            print(" No manual labels found! Please fill the 'manual_label' column first.")
            return

        y_true = df['manual_label']
        y_pred = df['model_prediction']

        # Overall accuracy
        correct = (y_pred == y_true).sum()
        accuracy = correct / len(df)

        print("\n" + "="*70)
        print("MANUAL EVALUATION RESULTS")
        print("="*70)
        print(f"Total evaluated: {len(df)}")
        print(f"Correct predictions: {correct}")
        print(f"Accuracy: {accuracy:.2%}")

        # **ADD THIS: Confusion Matrix**
        print("\n" + "="*70)
        print("CONFUSION MATRIX")
        print("="*70)
        cm = confusion_matrix(y_true, y_pred, labels=[
                            'Negative', 'Neutral', 'Positive'])
        cm_df = pd.DataFrame(cm,
                            index=['Actual Neg', 'Actual Neu', 'Actual Pos'],
                            columns=['Pred Neg', 'Pred Neu', 'Pred Pos'])
        print(cm_df)

        # **ADD THIS: Detailed Classification Report**
        print("\n" + "="*70)
        print("PER-CLASS METRICS")
        print("="*70)
        print(classification_report(y_true, y_pred,
                                    labels=['Negative', 'Neutral', 'Positive'],
                                    target_names=['Negative', 'Neutral', 'Positive']))

        # Show errors
        errors = df[y_pred != y_true]
        print(f"\n{'='*70}")
        print(f"ERRORS: {len(errors)}/{len(df)} ({len(errors)/len(df):.1%})")
        print("="*70)

        # **ADD THIS: Error breakdown by actual class**
        for label in ['Negative', 'Neutral', 'Positive']:
            label_errors = errors[errors['manual_label'] == label]
            if len(label_errors) > 0:
                print(f"\n{label.capitalize()} misclassified as:")
                for pred in label_errors['model_prediction'].value_counts().items():
                    print(f"  → {pred[0]}: {pred[1]} times")

        print("\nSample errors:")
        for idx, row in errors.head(5).iterrows():
            print(f"\nText: {row['text'][:80]}...")
            print(
                f"Predicted: {row['model_prediction']}, Actual: {row['manual_label']}")

        # Save results with confusion matrix
        results = {
            'total_evaluated': len(df),
            'accuracy': accuracy,
            'correct': int(correct),
            'confusion_matrix': cm.tolist(),
            'per_class': {}
        }

        for label in ['Negative', 'Neutral', 'Positive']:
            label_data = df[df['manual_label'] == label]
            if len(label_data) > 0:
                label_correct = (
                    label_data['model_prediction'] == label_data['manual_label']).sum()
                results['per_class'][label] = {
                    'count': len(label_data),
                    'correct': int(label_correct),
                    'accuracy': label_correct/len(label_data)
                }

        with open('src/test/manual_evaluation_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("\nResults saved to 'src/test/manual_evaluation_results.json'")

if __name__ == "__main__":

    evaluator = ManualEvaluation(sample_size=100)

    if len(sys.argv) > 1 and sys.argv[1] == 'manual':
        # Compare with your manual labels
        evaluator.calculate_accuracy_from_manual_labels()
    else:
        # Generate CSV for manual review
        evaluator.predict_and_save_for_manual_review()
