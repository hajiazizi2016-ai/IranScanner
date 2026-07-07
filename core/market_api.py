import requests


class MarketAPI:

    BASE = "https://cdn.tsetmc.com/api"

    def __init__(self):

        print("Market API initialized")

    def get_static_data(self):

        url = f"{self.BASE}/StaticData/GetStaticData"

        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        return r.json()

    def get_market_overview(self):

        url = f"{self.BASE}/MarketData/GetMarketOverview/0"

        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        return r.json()