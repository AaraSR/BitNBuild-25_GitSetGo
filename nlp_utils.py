# nlp_utils.py
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_reviews(reviews):
    """Analyze reviews and return insights"""
    texts = [r["text"] for r in reviews if r["text"].strip()]
    results = sentiment_pipeline(texts, truncation=True)

    enriched = []
    for r, res in zip(reviews, results):
        r["sentiment"] = res["label"]
        enriched.append(r)

    total = len(enriched)
    pos = sum(1 for r in enriched if "POS" in r["sentiment"].upper())
    neg = sum(1 for r in enriched if "NEG" in r["sentiment"].upper())
    neu = total - pos - neg

    # Keyword extraction
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X = vectorizer.fit_transform(texts)
    scores = np.asarray(X.sum(axis=0)).ravel()
    terms = np.array(vectorizer.get_feature_names_out())
    top_keywords = terms[np.argsort(scores)[::-1][:15]]

    summary = f"Users love: {', '.join(top_keywords[:3])}. ⚠️ Complaints: {', '.join(top_keywords[-3:])}."

    return {
        "total": total,
        "positive": pos,
        "negative": neg,
        "neutral": neu,
        "keywords": top_keywords.tolist(),
        "summary": summary,
        "reviews": enriched
    }