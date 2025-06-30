import re
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel, PeftConfig
import torch
import requests
from bs4 import BeautifulSoup

# ====== SETTINGS ======
BASE_MODEL_NAME = "t5-small"
FINETUNED_MODEL_PATH = "LORA/t5_small_summarizer_2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FMP_API_KEY = "pwm4EP6mJg6p3Ys2STFagWEkQMD0NqD3"
DEFAULT_KEYWORDS = ["Tesla", "Google", "Apple", "Microsoft", "Amazon", "Meta", 
                   "Nvidia", "Alphabet", "Netflix", "Disney", "Elon Musk", 
                   "Tim Cook", "AI"]

@st.cache_resource(show_spinner=False)
def load_models():
    base_model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL_NAME).to(DEVICE)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
    try:
        peft_config = PeftConfig.from_pretrained(FINETUNED_MODEL_PATH)
        finetuned_base = AutoModelForSeq2SeqLM.from_pretrained(peft_config.base_model_name_or_path)
        finetuned_model = PeftModel.from_pretrained(finetuned_base, FINETUNED_MODEL_PATH).to(DEVICE)
    except Exception as e:
        st.warning(f"Fine-tuned model not loaded: {e}")
        finetuned_model = None
    return tokenizer, base_model, finetuned_model


def summarize(text, model, tokenizer):
    inputs = tokenizer("summarize: " + text, return_tensors="pt", truncation=True, padding=True).to(DEVICE)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(output[0], skip_special_tokens=True)


def clean_html_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    for p in soup.find_all('p'):
        p.append('\n\n')
    text = soup.get_text()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines).strip()


def parse_fmp_articles():
    url = f"https://financialmodelingprep.com/api/v3/fmp/articles?page=0&size=20&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        articles = []
        for article in response["content"]:
            clean_content = clean_html_text(article["content"])
            articles.append({
                "title": article["title"],
                "date": article["date"],
                "content": clean_content,
                "tickers": article["tickers"].split(":")[1],
                "image": article["image"],
                "link": article["link"],
                "author": article["author"],
                "source": article["site"]
            })
        return articles
    except Exception as e:
        st.error(f"Error fetching articles: {e}")
        return []

def contains_keywords(text, keywords):
    """Check if text contains any of the keywords (case-insensitive)"""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

def parse_user_input(input_str):
    """Parse user input that may contain commas, spaces, or both as separators"""
    if not input_str:
        return []
    
    # Split by commas first, then split each part by spaces
    parts = []
    for item in input_str.split(','):
        parts.extend(item.split())
    
    # Remove empty strings and strip whitespace
    return [item.strip() for item in parts if item.strip()]

# ====== STREAMLIT UI ======
st.set_page_config(page_title="News Summarizer Feed", layout="centered")
st.title("🗞️ News Feed with AI Summarization")

if "feed" not in st.session_state:
    st.session_state.feed = []

use_finetuned = st.checkbox("Use fine-tuned model", value=True)
tokenizer, base_model, finetuned_model = load_models()
model_to_use = finetuned_model if (use_finetuned and finetuned_model is not None) else base_model

col1, col2 = st.columns(2)
with col1:
    user_tickers = st.text_input(
        "Your portfolio tickers", 
        placeholder="AAPL, GOOGL, NVDA",
        help="Enter tickers separated by commas or spaces"
    )
with col2:
    user_keywords = st.text_input(
        "Keywords to watch for", 
        placeholder="Elon Musk, Bill Gates, Linus Torvalds",
        help="Enter keywords separated by commas or spaces"
    )

# Add default keywords as checkboxes
default_keywords = st.multiselect(
    "Add default keywords",
    options=DEFAULT_KEYWORDS,
    default=["Netflix", "Tesla"],
    help="Select commonly used keywords to include"
)

with st.form("news_form"):
    user_input = st.text_area("📝 Paste or write a news article:", height=200)
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    with st.spinner("Generating summary..."):
        summary = summarize(user_input, model_to_use, tokenizer)
    st.session_state.feed.insert(0, {"text": user_input, "summary": summary})

if st.button("📡 Fetch news from FMP"):
    # Process user inputs
    tickers = [t.upper() for t in parse_user_input(user_tickers)]
    custom_keywords = parse_user_input(user_keywords)
    all_keywords = list(set(default_keywords + custom_keywords))  # Remove duplicates
        
    fmp_articles = parse_fmp_articles()
    
    matched_articles = []
    for article in fmp_articles:
        # Check if article has matching tickers
        ticker_match = article["tickers"] in tickers if tickers else False
        
        # Check if article content contains any keywords
        content_to_check = f"{article['title']}" #{article['content']}"
        keyword_match = contains_keywords(content_to_check, all_keywords) if all_keywords else False
        
        if ticker_match or keyword_match:
            matched_articles.append(article)

    with st.spinner(f"Summarizing {len(matched_articles)} relevant articles..."):
        for article in matched_articles:
            summary = summarize(article["content"], model_to_use, tokenizer)
            st.session_state.feed.insert(0, {
                "title": article["title"],
                "text": article["content"],
                "summary": summary,
                "source": article.get("source", ""),
                "date": article.get("date", ""),
                "matched_by": "Ticker" if ticker_match else "Keyword"
            })

# ====== DISPLAY FEED ======
st.markdown("---")
st.subheader("📰 Summarized News Feed")

for item in st.session_state.feed:
    with st.container():
        header = f"**{item.get('title', 'No title')}**"
        if 'date' in item:
            header += f" ({item['date']})"
        
        st.markdown(header)
        st.text(item['summary'])

        with st.expander("Show original article"):
            st.markdown(f"<div style='color:gray; font-size:0.9em'>{item['text']}</div>", unsafe_allow_html=True)
        st.markdown("---")