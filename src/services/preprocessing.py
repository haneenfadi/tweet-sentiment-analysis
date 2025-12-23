import re

class TweetDataProcessor:
 
    def __init__(self):
        self.url_pattern = r'http\S+|www\S+|https\S+'
        self.clean_pattern = r'[^A-Za-z\s]'

    def remove_urls(self, text: str) -> str:
        return re.sub(self.url_pattern, ' ', text)

    def clean_text(self, text: str) -> str:
        text = re.sub(self.clean_pattern, '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()

    def preprocess(self, text: str) -> str:
        """
        Full preprocessing pipeline for ONE text.
        """
        text = self.remove_urls(text)
        text = self.clean_text(text)
        return text

