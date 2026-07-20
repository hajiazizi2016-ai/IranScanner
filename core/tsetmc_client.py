import requests


class TSETMCClient:

    API_BASE = "https://cdn.tsetmc.com/api"

    OLD_BASE = "https://old.tsetmc.com/tsev2/data"

    def __init__(self):

        self.session = requests.Session()

        # این کلاینت همیشه باید مستقیم به TSETMC وصل بشه، حتی اگر
        # ویندوز/سایفون یک پراکسی سیستمی تنظیم کرده باشد (که فقط برای
        # تلگرام لازم است، نه برای TSETMC که یک سایت داخلی ایران است).
        self.session.trust_env = False
        self.session.proxies = {}

        self.session.headers.update({

            "User-Agent": "Mozilla/5.0",

            "Accept": "application/json"

        })

        print("TSETMC Client initialized")

    def get(self, api):

        url = self.API_BASE + api

        r = self.session.get(url, timeout=30)

        r.raise_for_status()

        return r.json()

    def get_old(self, path):

        url = self.OLD_BASE + path

        r = self.session.get(url, timeout=30)

        r.raise_for_status()

        return r.text


