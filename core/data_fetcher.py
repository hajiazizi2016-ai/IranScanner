import requests


class DataFetcher:

    def __init__(self):
        self.url = "https://www.tsetmc.com/Loader.aspx?ParTree=111C1417"

    def get_market_watch(self):

        print("Fetching TSETMC API data...")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            r = requests.get(
                self.url,
                headers=headers,
                timeout=15
            )

            r.encoding = "utf-8"

            return r.text

        except Exception as e:
            print(e)
            return ""