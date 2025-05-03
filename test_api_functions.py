import unittest
from unittest.mock import patch

from apis.stocks import get_stock_history
from apis.crypto import get_crypto_prices
from apis.news import get_market_news
from apis.exchange import get_exchange_rates_all

class TestAPIFunctions(unittest.TestCase):

    @patch('apis.stocks.requests.get')
    def test_get_stock_data(self, mock_get):
        # Sample fake response
        mock_response = {
            "Time Series (Daily)": {
                "2024-05-03": {"4. close": "173.50"},
                "2024-05-02": {"4. close": "172.00"},
                "2024-05-01": {"4. close": "170.50"},
                "2024-04-30": {"4. close": "169.00"},
                "2024-04-29": {"4. close": "171.00"},
                "2024-04-28": {"4. close": "172.75"},
                "2024-04-27": {"4. close": "173.80"},
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        dates, prices = get_stock_history("AAPL")

        self.assertEqual(len(dates), 7)
        self.assertEqual(len(prices), 7)
        self.assertTrue(all(isinstance(p, float) for p in prices))

    @patch('apis.crypto.requests.get')
    def test_get_crypto_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Realtime Currency Exchange Rate": {
                "5. Exchange Rate": "64000.00"
            }
        }

        result = get_crypto_prices(["BTC", "ETH"])

        self.assertIsInstance(result, dict)
        self.assertIn("BTC", result)
        self.assertIn("ETH", result)
        self.assertEqual(result["BTC"], 64000.00)
        self.assertEqual(result["ETH"], 64000.00)

    def test_get_market_news(self):
        # Assuming mock data, no external request
        result = get_market_news()
        self.assertIsInstance(result, list)
        self.assertTrue(all('title' in item and 'source' in item for item in result))

    @patch('apis.exchange.requests.get')
    def test_get_exchange_rates(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "rates": {"EUR": 0.93, "JPY": 155.3, "GBP": 0.81},
            "base": "USD"
        }
        result = get_exchange_rates_all("USD")
        self.assertIn("EUR", result)
        self.assertIn("JPY", result)

if __name__ == '__main__':
    unittest.main()
