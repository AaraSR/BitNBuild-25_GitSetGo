# app.py
import streamlit as st
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from scraper import scrape_reviews_from_url
from nlp_utils import analyze_reviews

st.set_page_config(page_title="Review Radar", layout="wide")
st.title("🔎 Review Radar — Product Review Analyzer")

# Inputs
col1, col2 = st.columns(2)
url1 = col1.text_input("Product URL 1")
url2 = col2.text_input("Product URL 2 (optional)")
uploaded = st.file_uploader("Upload Reviews JSON", type=["json"])
max_reviews = st.slider("Max reviews to analyze", 10, 200, 50)

if st.button("Analyze"):
    reviews1, reviews2 = [], []

    if uploaded:
        reviews1 = json.load(uploaded)
    elif url1:
        st.info("🔄 Scraping product 1...")
        reviews1 = scrape_reviews_from_url(url1, max_reviews)
        if url2:
            st.info("🔄 Scraping product 2...")
            reviews2 = scrape_reviews_from_url(url2, max_reviews)
    else:
        with open("sample_reviews.json") as f:
            reviews1 = json.load(f)

    if not reviews1:
        st.error("No reviews found.")
        st.stop()

    # Analyze
    result1 = analyze_reviews(reviews1)
    result2 = analyze_reviews(reviews2) if reviews2 else None

    # --- Product 1 ---
    st.header(" Product 1 Insights")
    st.metric("Total Reviews", result1["total"])
    st.metric("Positive", result1["positive"])
    st.metric("Negative", result1["negative"])
    st.metric("Neutral", result1["neutral"])
    st.subheader("Summary")
    st.write(result1["summary"])

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie([result1["positive"], result1["negative"], result1["neutral"]],
           labels=["Positive", "Negative", "Neutral"],
           autopct="%1.1f%%", colors=["green","red","gray"])
    st.pyplot(fig)

    # Word Cloud
    st.subheader("Word Cloud of Keywords")
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(result1["keywords"]))
    st.image(wc.to_array())

    # --- Product 2 (if provided) ---
    if result2:
        st.header(" Product 2 Insights")
        st.metric("Total Reviews", result2["total"])
        st.metric("Positive", result2["positive"])
        st.metric("Negative", result2["negative"])
        st.metric("Neutral", result2["neutral"])
        st.subheader("Summary")
        st.write(result2["summary"])

        # Comparison chart
        st.subheader(" Comparison")
        fig2, ax2 = plt.subplots()
        labels = ["Positive", "Negative", "Neutral"]
        ax2.bar(labels, [result1["positive"], result1["negative"], result1["neutral"]],
                alpha=0.7, label="Product 1", color='blue')
        ax2.bar(labels, [result2["positive"], result2["negative"], result2["neutral"]],
                alpha=0.7, label="Product 2", color='orange')
        ax2.legend()
        st.pyplot(fig2)
