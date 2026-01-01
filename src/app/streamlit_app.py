# ==============================
# IMPORTS
# ==============================
import streamlit as st

import sys
from pathlib import Path

# Count how many .parent you need based on file depth
project_root = Path(__file__).resolve().parent.parent.parent

# Add to path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.services.pipeline import Pipeline


# ==============================
# FUNCTIONS / MODEL LOADING
# ==============================

@st.cache_resource
def load_model():
    """Load the sentiment analysis pipeline once and cache it."""
    return Pipeline()


# ==============================
# STREAMLIT CONFIG
# ==============================
st.set_page_config(
    page_title="Tweet Sentiment Analysis",
    page_icon="💬",
    layout="centered",
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f3f4f6 0%, #e0e7ff 100%);
        color: #333;
        font-family: "Segoe UI", sans-serif;
    }
    .title {
        text-align: center;
        color: #3b82f6;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 14px 16px;
        font-size: 1rem;
        transition: border-color 0.3s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    div.stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-size: 1.05rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .result-box {
        background: white;
        border-radius: 16px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .result {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 10px;
    }
    .result-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER / TITLE
# ==============================
st.markdown('<div class="title">💬 Tweet Sentiment Analyzer</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Analyze the sentiment of any tweet instantly. Find out if it\'s positive, neutral, or negative.</div>',
    unsafe_allow_html=True
)

# ==============================
# INPUT
# ==============================
tweet = st.text_input(
    "Enter your tweet:",
    placeholder="e.g., Just finished an amazing project! Really proud of what we accomplished.",
    label_visibility="collapsed"
)

# ==============================
# LOAD MODEL
# ==============================
model = load_model()  # Load once globally

# ==============================
# ANALYZE BUTTON
# ==============================
if st.button("🔍 Analyze Sentiment"):
    if not tweet.strip():
        st.warning("⚠️ Please enter a tweet to analyze.")
    else:
        with st.spinner("Analyzing sentiment..."):
            sentiment = model.predict(tweet)

        # Define colors and emojis
        sentiment_config = {
            "Positive": {"color": "#22c55e", "emoji": "😊", "bg": "#f0fdf4"},
            "Negative": {"color": "#ef4444", "emoji": "😞", "bg": "#fef2f2"},
            "Neutral": {"color": "#eab308", "emoji": "😐", "bg": "#fefce8"}
        }

        config = sentiment_config.get(sentiment, sentiment_config["Neutral"])

        # Display result
        st.markdown(f"""
            <div class="result-box" style="background: {config['bg']}; border: 2px solid {config['color']}20;">
                <div class="result-label">Detected Sentiment</div>
                <div class="result" style="color:{config['color']};">
                    {config['emoji']} {sentiment}
                </div>
            </div>
        """, unsafe_allow_html=True)
