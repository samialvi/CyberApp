import requests
import os

API_KEY = os.getenv("NEWS_API_KEY") or "8461e016c3a34e0ca0b4f81d324ab3b0"

def get_market_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?category=business&apiKey={API_KEY}&pageSize=5"
        res = requests.get(url)
        articles = res.json().get("articles", [])
        return [{"title": a["title"], "source": a["source"]["name"]} for a in articles]
    except Exception:
        return [{"title": "Failed to load news.", "source": "N/A"}]

