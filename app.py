import streamlit as st
import os

from services.youtube_service import fetch_transcript
from services.gemini_service import generate_article
from services.pdf_service import create_pdf
from utils.text_cleaner import clean_text

st.set_page_config(page_title="YouTube Summarizer", layout="centered")

st.title("📺 YouTube Video Summarizer")
st.write("Paste a YouTube URL and generate a structured article + PDF.")

url = st.text_input("🔗 Enter YouTube URL")

if st.button("Generate Article"):

    if not url:
        st.warning("Please enter a YouTube URL")
        st.stop()

    if "youtube.com" not in url and "youtu.be" not in url:
        st.error("Invalid YouTube URL")
        st.stop()

    try:
        with st.spinner("Fetching transcript..."):
            transcript = fetch_transcript(url)

        with st.spinner("Cleaning text..."):
            cleaned = clean_text(transcript)

        with st.spinner("Generating article using Gemini..."):
            article = generate_article(cleaned)

        os.makedirs("output", exist_ok=True)

        txt_path = "output/article.txt"
        pdf_path = "output/article.pdf"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(article)

        create_pdf(article, pdf_path)

        st.success("✅ Done!")

        st.subheader("📝 Generated Article")
        st.write(article)

        # Download buttons
        with open(txt_path, "rb") as f:
            st.download_button("📄 Download TXT", f, "article.txt")

        with open(pdf_path, "rb") as f:
            st.download_button("📕 Download PDF", f, "article.pdf")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")