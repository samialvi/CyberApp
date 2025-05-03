import requests
import os

API_KEY = os.getenv("ALPHA_VANTAGE_KEY") or "38279768c08cd962ff7f344a"

def get_stock_history(symbol="AAPL"):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY" \
              f"&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
        res = requests.get(url)
        data = res.json()
        time_series = data["Time Series (Daily)"]
        dates = list(time_series.keys())[:7][::-1]
        prices = [float(time_series[date]["4. close"]) for date in dates]
        return dates, prices
    except Exception as e:
        return ["Error"], [0]

