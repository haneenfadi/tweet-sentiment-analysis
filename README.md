# 🐦 Tweet Sentiment Analysis with Hugging Face

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)

## 📖 About

A Python project that analyzes the sentiment of tweets using a pretrained Hugging Face model (`cardiffnlp/twitter-xlm-roberta-base-sentiment`).

**Supports three sentiment classes:**
- 😊 **Positive** (label: 2)
- 😐 **Neutral** (label: 1)
- 😞 **Negative** (label: 0)

The project includes both a **FastAPI backend** for API integration and a beautiful **Streamlit interface** for interactive usage.

---
## Features

- **Accurate sentiment prediction** using a state-of-the-art Hugging Face model  
- **Robust text preprocessing pipeline**, including:
  - Removal of URLs and mentions  
  - Cleaning of special characters and numbers  
  - Text normalization (lowercasing)  
- **FastAPI-based API** for seamless integration  
- **Modern Streamlit interface** with real-time sentiment visualization  
- **Secure API access** using password-based authentication  
- **Well-structured project architecture** following OOP principles  


---

##  Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/haneenfadi/tweet-sentiment-analysis.git
cd tweet-sentiment-analysis
```

2. **Create a virtual environment (recommended):**

```bash
python -m venv venv
```

3. **Activate the virtual environment:**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

5. **Set up environment variables:**

Create a `.env` file in the project root (copy from `.env.example`):

```bash
# Windows
copy src\.env.example .env

# Mac/Linux
cp src/.env.example .env
```

Then edit `.env` and set your authentication password:

```env
# .env
API_AUTH_PASSWORD=your_secure_password_here
```

> ⚠️ **IMPORTANT:** Never commit your `.env` file to GitHub! It's already in `.gitignore`.

---

## 💻 Usage

### Option 1: Streamlit Interface (Recommended for Testing)

Run the Streamlit app:

```bash
streamlit run src/app/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

**Features:**
- 💬 Enter any tweet or text
- 🔍 Get instant sentiment analysis
- 🎨 Beautiful gradient UI with emoji indicators

### Option 2: FastAPI Backend (For API Integration)

1. **Start the FastAPI server:**

```bash
uvicorn src.app.api:app --reload
```

The API will be available at `http://localhost:8000`

2. **API Documentation:**

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

3. **Make a prediction request:**

**Example using `curl`:**
```bash
curl --location 'http://localhost:8000/api/v1/sentiment/predict' \
--header 'Content-Type: application/json' \
--header 'API_AUTH_PASSWORD: your_secure_password_here' \
--data-raw '{
    "text": "@switchfoot http://twitpic.com/2y1zl - Awww, that'\''s a bummer. You shoulda got David Carr of Third Day to do it. ;D"
  }'

```

**Expected Response:**
```json
{
    "text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer. You shoulda got David Carr of Third Day to do it. ;D",
    "sentiment": "Negative"
}
```

---

## 📊 Dataset

The preprocessing pipeline is based on the Twitter Sentiment Analysis dataset from Kaggle.

**Dataset Link:** [Twitter Sentiment Analysis Dataset](https://www.kaggle.com/datasets/raj713335/twittesentimentanalysis/data)

**Sample Tweet for Testing:**
```
"@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer. You shoulda got David Carr of Third Day to do it. ;D"
```

---

## 🤖 Model Details

**Model:** `cardiffnlp/twitter-xlm-roberta-base-sentiment`

**Architecture:** XLM-RoBERTa Base  
**Task:** Sentiment Analysis (Text Classification)  
**Languages:** Multilingual (optimized for English tweets)

**Label Mapping:**
| Label | Sentiment | Emoji |
|-------|-----------|-------|
| 0     | Negative  | 😞    |
| 1     | Neutral   | 😐    |
| 2     | Positive  | 😊    |

---

## 🗂 Project Structure

```
tweet-sentiment-analysis/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
└── src/                        # Source code package
    ├── __init__.py
    ├── app/                    # Application layer (UI & API)
    │   ├── __init__.py
    │   ├── api.py              # FastAPI application
    │   └── streamlit_app.py    # Streamlit interface
    ├── data/                   # Data storage
    │   └── tweets.csv          # Sample dataset
    ├── routes/                 # API routes
    │   ├── base.py
    │   └── predict.py
    ├── services/               # Business logic layer
    │   ├── __init__.py
    │   ├── pipeline.py         # Main prediction pipeline
    │   ├── preprocessing.py    # Text preprocessing
    │   └── tweets_analysis.py  # Sentiment analysis logic
    └── utils/                  # Utilities layer
        ├── __init__.py
        ├── config.py           # Configuration management (stores the model_id to allow easy model changes in the future)
        └── schemas.py          # Pydantic schemas for request and response validation
```

## ⚙️ Configuration

### Environment Variables (`.env`)

Create a `.env` file in the project root with the following:

```env
# API Authentication
API_AUTH_PASSWORD=your_secure_password_here

```

> 📝 **Note:** A `.env.example` file is provided as a template. Copy it and add your actual credentials.

---

## 🔒 Security Notes

1. **Never commit your `.env` file** - it contains sensitive credentials
2. **Use strong passwords** for `API_AUTH_PASSWORD`
3. **Keep your dependencies updated** - run `pip install --upgrade -r requirements.txt` regularly
4. **API authentication** is required for all prediction endpoints

---

## 👤 Author

**Haneen Fadi**

- GitHub: ## 👤 Author

**Haneen Fadi**

- GitHub: [@haneenfadi](https://github.com/haneenfadi)
- Email: haneenqutishat03@gmail.com
