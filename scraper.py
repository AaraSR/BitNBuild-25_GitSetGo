# scraper.py
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def scrape_reviews_from_url(url, max_reviews=50):
    """Scrape reviews from Amazon or Flipkart"""
    if "amazon." in url:
        return _scrape_amazon(url, max_reviews)
    elif "flipkart." in url:
        return _scrape_flipkart(url, max_reviews)
    else:
        raise ValueError("Only Amazon/Flipkart URLs supported")

def _scrape_amazon(url, max_reviews):
    reviews = []
    page = 1
    while len(reviews) < max_reviews:
        review_url = url + f"&pageNumber={page}"
        r = requests.get(review_url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        review_divs = soup.select(".review-text-content")
        if not review_divs: break
        for div in review_divs:
            reviews.append({"text": div.get_text(strip=True)})
            if len(reviews) >= max_reviews: break
        page += 1
        time.sleep(1)
    return reviews

def _scrape_flipkart(url, max_reviews):
    reviews = []
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    review_divs = soup.select("div._16PBlm")
    for div in review_divs[:max_reviews]:
        reviews.append({"text": div.get_text(strip=True)})
    return reviews