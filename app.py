import streamlit as st
import json
from scraper import scrape_reviews_from_url
from nlp_utils import analyze_reviews
import altair as alt
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="ReviewRadar", page_icon="📡")

# --- Sidebar ---
with st.sidebar:
    st.header("About ReviewRadar")
    st.write("""
        ReviewRadar uses NLP to analyze product reviews from e-commerce sites. 
        Get quick insights without the manual effort!
    """)
    st.header("Instructions")
    st.write("""
        1.  Paste an Amazon or Flipkart product URL.
        2.  Click 'Analyze'.
        3.  View the sentiment breakdown and top keywords.
    """)

# --- Main App ---
st.title("📡 ReviewRadar")
st.subheader("Your go-to for quick and insightful product review analysis.")

# --- URL Input ---
url = st.text_input("Enter Product URL (Amazon or Flipkart)", "")

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Analyze Reviews"):
        if url:
            try:
                with st.spinner("Scraping and analyzing reviews... This may take a moment."):
                    reviews = scrape_reviews_from_url(url)
                    if reviews:
                        st.session_state.analysis_results = analyze_reviews(reviews)
                    else:
                        st.warning("Could not scrape any reviews. Check the URL or try another product.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a URL.")

with col2:
    if st.button("Load Sample Data"):
        with open("sample_reviews.json", "r") as f:
            reviews = json.load(f)
        st.session_state.analysis_results = analyze_reviews(reviews)


# --- Display Results ---
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    st.header("Analysis Dashboard")

    # --- Metrics ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", results["total"])
    col2.metric("Positive", f"{results['positive']} ({results['positive']/results['total']:.1%})")
    col3.metric("Negative", f"{results['negative']} ({results['negative']/results['total']:.1%})")
    col4.metric("Neutral", f"{results['neutral']} ({results['neutral']/results['total']:.1%})")

    # --- Charts ---
    chart_data = pd.DataFrame({
        'Sentiment': ['Positive', 'Negative', 'Neutral'],
        'Count': [results['positive'], results['negative'], results['neutral']]
    })
    
    c = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Sentiment', sort=None),
        y='Count',
        color='Sentiment'
    ).properties(
        title="Sentiment Distribution"
    )
    
    st.altair_chart(c, use_container_width=True)

    # --- Keywords & Summary ---
    st.subheader("Summary & Top Keywords")
    st.info(results["summary"])
    
    st.subheader("Top Keywords")
    st.write(results["keywords"])

    # --- Raw Reviews ---
    with st.expander("View Analyzed Reviews"):
        st.dataframe(pd.DataFrame(results["reviews"]))
