# from fastapi import APIRouter, Header, HTTPException
# from src.services.pipeline import Pipeline
# from src.utils.schemas import TweetRequest
# from loguru import logger
# from dotenv import load_dotenv
# import os

# load_dotenv()
# API_AUTH_PASSWORD = os.environ.get("API_AUTH_PASSWORD", "")
# pipeline = Pipeline()

# sentiment_router = APIRouter(
#     prefix="/api/v1/sentiment",
#     tags=["sentiment_analysis"]
# )


# @sentiment_router.post("/predict")
# async def predict_sentiment(
#     request: TweetRequest,
#     api_auth_password: str = Header(...)  # <-- read password from header
# ):
#     # Check client password
#     if api_auth_password != API_AUTH_PASSWORD:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     logger.info("Received sentiment prediction request")
#     try:
#         logger.info(f"Input text length: {len(request.text)}")

#         sentiment = pipeline.predict(request.text)
#         logger.info(f"Prediction result: {sentiment}")

#         return {
#             "text": request.text,
#             "sentiment": sentiment,
#         }

#     except Exception as e:
#         logger.error(f"Prediction failed: {str(e)}")
#         raise HTTPException(status_code=500, detail="Prediction failed")

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.pipeline import Pipeline
from src.utils.schemas import TweetRequest
from loguru import logger
from dotenv import load_dotenv
import os

load_dotenv()
API_AUTH_PASSWORD = os.environ.get("API_AUTH_PASSWORD", "")
pipeline = Pipeline()

security = HTTPBearer()

sentiment_router = APIRouter(
    prefix="/api/v1/sentiment",
    tags=["sentiment_analysis"]
)


@sentiment_router.post("/predict")
async def predict_sentiment(
    request: TweetRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify token
    if not API_AUTH_PASSWORD:
        logger.error("API_AUTH_PASSWORD not set in environment")
        raise HTTPException(status_code=500, detail="Server configuration error")
    
    if credentials.credentials != API_AUTH_PASSWORD:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    logger.info("Received sentiment prediction request")
    try:
        logger.info(f"Input text length: {len(request.text)}")

        sentiment = pipeline.predict(request.text)
        logger.info(f"Prediction result: {sentiment}")

        return {
            "text": request.text,
            "sentiment": sentiment,
        }

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")