import requests
import os

API_KEY = os.getenv("ALPHA_VANTAGE_KEY") or "HW5MHKAG4FTAGX4D"

def get_crypto_prices(symbols=["BTC", "ETH", "XRP"]):
    prices = {}
    for symbol in symbols:
        try:
            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE" \
                  f"&from_currency={symbol}&to_currency=USD&apikey={API_KEY}"
            res = requests.get(url)
            data = res.json()
            rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            prices[symbol] = float(rate)
        except:
            prices[symbol] = 0
    return prices

