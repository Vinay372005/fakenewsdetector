import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

st.set_page_config(page_title="Fake News Detector", layout="centered")
st.title("🕵️ Fake News Detector")
st.markdown("Paste a news article URL and get a verdict on its authenticity!")

openai.api_key = st.text_input("OpenAI API Key", type="password")
url = st.text_input("Article URL:")

def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = "\n".join([para.get_text() for para in paragraphs])
    return article_text[:4000]

def analyze_article_with_gpt(article_text):
    prompt = f"""Analyze the following news article and determine whether it appears to be fake or trustworthy.
Provide a clear verdict ("Likely Fake" or "Likely Real") and explain your reasoning:

{article_text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert fact-checker."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700
    )
    return response['choices'][0]['message']['content']

if url and openai.api_key:
    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            try:
                text = extract_article_text(url)
                result = analyze_article_with_gpt(text)
                st.subheader("🧠 GPT Verdict")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
