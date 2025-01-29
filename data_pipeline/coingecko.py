import pandas as pd
import requests


class CoinGeckoFetcher:
    BASE_URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    @staticmethod
    def fetch_historical_data(
        coin_id="bitcoin", vs_currency="usd", days=365):
        url = CoinGeckoFetcher.BASE_URL.format(coin_id=coin_id)
        params = {
            "vs_currency": vs_currency,
            "days": days,
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()["prices"]
            df = pd.DataFrame(data, columns=["timestamp", "price"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")
