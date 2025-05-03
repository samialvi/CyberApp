import requests
import os

API_KEY = os.getenv("EXCHANGE_API_KEY") or "38279768c08cd962ff7f344a"

def get_exchange_rates_all(base="USD", targets=None):
    targets = targets or ["EUR", "GBP", "JPY", "INR"]
    rates = {}
    for currency in targets:
        try:
            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE" \
                  f"&from_currency={base}&to_currency={currency}&apikey={API_KEY}"
            res = requests.get(url)
            data = res.json()
            rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            rates[currency] = float(rate)
        except:
            rates[currency] = 0
    return rates

