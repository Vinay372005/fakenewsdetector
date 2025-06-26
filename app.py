import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="Fake News Detector", layout="centered")
st.title("📰 Fake News Detector")

# Get OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# News input
news_text = st.text_area("📝 Paste a news article or headline:")

# Handle submission
if st.button("🔍 Check if it's Fake or Real"):
    if not news_text.strip():
        st.warning("Please enter some news content.")
    else:
        with st.spinner("Analyzing..."):
            prompt = (
                "You are a news fact-checking AI. Determine if the following news article is FAKE or REAL. "
                "Reply with 'Fake' or 'Real' followed by a short explanation.\n\n"
                f"News: {news_text}\n\n"
                "Answer:"
            )

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=150
                )

                result = response.choices[0].message.content.strip()
                st.success("✅ Result:")
                st.markdown(f"**{result}**")

            except Exception as e:
                st.error(f"Error: {str(e)}")
