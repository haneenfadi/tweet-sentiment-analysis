import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.utils.config import model_id_dict
class SentimentModel:
    def __init__(self, model_id=model_id_dict["model_1"]):
        self.model_id = model_id
        self.load_model()
    
    def load_model(self):
        """
        Load tokenizer and model once.
        
        """
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id,use_fast=False,trust_remote_code=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_id,trust_remote_code=True)
        
        return self

    def predict_sentiment(self, text):
        """
        Predict sentiment of a single text using Hugging Face model.
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

        with torch.no_grad():        # Get model prediction
            logits = self.model(**inputs).logits
        predicted_class = torch.argmax(logits, dim=1).item()
        label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
        return label_map.get(predicted_class, "Unknown")





