from src.services.preprocessing import TweetDataProcessor
from src.services.tweets_analysis import SentimentModel
from src.utils.config import model_id_dict

class Pipeline:
    """
    Full pipeline: text preprocessing + sentiment prediction
    """
    def __init__(self, model_id=model_id_dict["model_4"]):
        self.preprocessor = TweetDataProcessor()
        self.model = SentimentModel(model_id=model_id)

    def predict(self, text:str):
        """
        Accept a single text or a list of texts.
        Returns sentiment(s) after preprocessing.
        """
        if isinstance(text, str):
            processed = self.preprocessor.preprocess(text)
            return self.model.predict_sentiment(processed)

        else:
            raise ValueError("Input must be a string or a list of strings")
