# Tweet Sentiment Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

Production-ready sentiment analysis system for tweets using the `DunnBC22/distilbert-base-uncased-US_Airline_Twitter_Sentiment_Analysis` model. Features dual deployment options with FastAPI REST API and Streamlit web interface.

---

## Technical Features

- **Preprocessing Pipeline:** URL removal, mention normalization, special character handling, text normalization
- **API Security:** Password-based authentication with environment variable configuration
- **Dual Interface:** RESTful API for integration, Streamlit UI for interactive testing
- **Container Support:** Docker and Docker Compose ready
- **Architecture:** Clean separation of concerns with services, routes, and utilities layers

---

## Model Architecture

**Base Model:** distilbert-base-uncased  
**Task:** Multi-class Text Classification (Sentiment Analysis)  
**Training:** Fine-tuned on Twitter sentiment data  
**Language Support:** English-only
**Fine-tuned on:** US Airline Twitter Sentiment dataset

**Classification Schema:**

| Label | Sentiment | Description |
|-------|-----------|-------------|
| 0     | Negative  | Critical feedback, complaints, dissatisfaction |
| 1     | Neutral   | Factual statements, questions, informational content |
| 2     | Positive  | Praise, recommendations, satisfaction |

---

## Demo

### Positive Sentiment
<p align="center">
  <img src="images/Positive.PNG" width="70%" />
</p>

### Neutral Sentiment
<p align="center">
  <img src="images/Neutral.PNG" width="70%" />
</p>

### Negative Sentiment
<p align="center">
  <img src="images/Negative.PNG" width="70%" />
</p>

---

## Dataset

pipeline designed for the [Twitter Sentiment Analysis Dataset](https://www.kaggle.com/datasets/raj713335/twittesentimentanalysis/data) 

**Note:** Only the text column was utilized. The original target labels were ignored as the goal was to build a custom three-class sentiment classifier (Negative, Neutral, Positive). The preprocessing pipeline was specifically tailored to handle tweet-specific features such as mentions, hashtags, URLs, treating the data as unlabeled input for real-world inference.

---
## Model Performance

**Evaluation on 100 manually labeled tweets:**

- Overall Accuracy: **91%**
- Macro F1-Score: **0.90**

| Class    | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| Negative | 0.91      | 0.96   | 0.93     |
| Neutral  | 0.91      | 0.91   | 0.91     |
| Positive | 0.91      | 0.81   | 0.86     |

---
## Installation

Clone the repository and set up environment:

```bash
git clone https://github.com/haneenfadi/tweet-sentiment-analysis.git
cd tweet-sentiment-analysis
```

### Local Development

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Docker Deployment

```bash
docker-compose up --build
```

### Environment Configuration

```bash
cp src/.env.example .env
```

Edit `.env`:
```env
API_AUTH_PASSWORD=your_secure_password_here
```

---

## Usage

### Streamlit Interface

```bash
streamlit run src/app/streamlit_app.py
```

Access at `http://localhost:8501`

### FastAPI Endpoint

```bash
uvicorn src.app.api:app 
```

API available at `http://localhost:8000`  
Interactive documentation: `http://localhost:8000/docs`

**Request Example:**

```bash
curl -X POST "http://localhost:8000/api/v1/sentiment/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization:Bearer your_secure_password_here" \
  -d '{
    "text": "@switchfoot http://twitpic.com/2y1zl - Awww, that'\''s a bummer. You shoulda got David Carr of Third Day to do it. ;D"
  }'
```

**Response:**
```json
{
  "text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer. You shoulda got David Carr of Third Day to do it. ;D",
  "sentiment": "Negative"
}
```

---

## Project Structure

```
tweet-sentiment-analysis/
│
├── Dockerfile                      # Container definition for deployment
├── docker-compose.yml              # Multi-container orchestration
├── .dockerignore                   # Docker build exclusions
├── .gitignore                      # Git tracking exclusions
├── .gitattributes                  # Git attribute configuration
├── .env.example                    # Environment variables template
├── requirements.txt                # Python package dependencies
├── README.md                       # Project documentation
│
├── images/                         # Visualization assets
│   ├── Negative.PNG
│   ├── Positive.PNG
│   └── Neutral.PNG
│
└── src/                            # Source code directory
    │
    ├── app/                        # Application layer
    │   ├── api.py                  # FastAPI REST endpoints
    │   └── streamlit_app.py        # Interactive web interface
    │
    ├── routes/                     # API routing
    │   ├── base.py                 # Base route handlers
    │   └── predict.py              # Prediction route definitions
    │
    ├── services/                   # Business logic layer
    │   ├── pipeline.py             # End-to-end prediction pipeline
    │   ├── preprocessing.py        # Text cleaning and normalization
    │   └── tweets_analysis.py      # Sentiment model 
    │
    ├── utils/                      # Utilities and helpers
    │   ├── config.py               # Configuration management
    │   └── schemas.py              # Pydantic data models
    │
    ├── data/                       
    │   └── tweets.csv              # Sample tweet dataset
    │
    └── test/                       # Testing suite
        ├── evaluate.py             # Model evaluation metrics
        ├── test_500_sample.py      # Sample-based testing
        └── test_model_vs_model.py  # Comparative model analysis
      
```

---

## Security

- Environment variables stored in `.env` (excluded from version control)
- API authentication required for all prediction endpoints
- Strong password requirements for production deployment
- Regular dependency updates recommended

---

## Author

**Haneen Fadi**  
GitHub: [@haneenfadi](https://github.com/haneenfadi)  
Email: haneenqutishat03@gmail.com

---
