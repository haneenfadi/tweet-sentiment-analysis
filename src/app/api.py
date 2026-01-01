from fastapi import FastAPI
from src.routes import base, predict
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_PASSWORD = os.environ.get("API_AUTH_PASSWORD", "")

app = FastAPI(
    title="Tweets Sentiment Analysis API",
    description="API for analyzing sentiment of tweets ",
)

# Configuration for authorization
if not AUTH_PASSWORD:
    raise EnvironmentError(
        "Missing required environment variable: API_AUTH_PASSWORD")
    
app.include_router(base.base_router)
app.include_router(predict.sentiment_router)
