import os
import time
import requests

from core.market_parser import MarketParser
from core.client_type_parser import ClientTypeParser


class MarketAPI:

    BASE_URLS = (
        "http://old.tsetmc.com/tsev2/data",
        "https://old.tsetmc.com/tsev2/data",
    )

    MARKET_URL = "/MarketWatchInit.aspx?h=0&r=0"
    CLIENTTYPE_URL = "/ClientTypeAll.aspx"

    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False

        self.tse_proxy = os.getenv("TSE_PROXY", "").strip()
        if self.tse_proxy:
            self.session.proxies.update({"http": self.tse_proxy, "https": self.tse_proxy})
            print("TSETMC proxy configured")
        else:
            self.session.proxies.clear()
            print("TSETMC direct connection")

        self.market_parser = MarketParser()
        self.client_parser = ClientTypeParser()
        self.market_cache = None
        self.client_cache = None
        self.market_time = 0
        self.client_time = 0
        self.timeout = 20
        self.retry = 3
        self.headers = {"User-Agent": "Mozilla/5.0", "Accept": "*/*", "Connection": "close"}
        print("Market API initialized")

    def _download(self, url):
        last_error = None
        bases = self.BASE_URLS if url.startswith("/") else ("",)
        for base_url in bases:
            target = base_url + url if url.startswith("/") else url
            for attempt in range(self.retry):
                try:
                    response = self.session.get(target, timeout=self.timeout, headers=self.headers)
                    response.raise_for_status()
                    return response.text
                except requests.RequestException as exc:
                    last_error = exc
                    if attempt < self.retry - 1:
                        time.sleep(1 + attempt)
        raise last_error

    def market(self):
        if self.market_cache is not None and time.time() - self.market_time < 5:
            return self.market_cache
        raw = self._download(self.MARKET_URL)
        self.market_cache = self.market_parser.parse(raw)
        self.market_time = time.time()
        return self.market_cache

    def client_type(self):
        if self.client_cache is not None and time.time() - self.client_time < 10:
            return self.client_cache
        raw = self._download(self.CLIENTTYPE_URL)
        self.client_cache = self.client_parser.parse(raw)
        self.client_time = time.time()
        return self.client_cache

    def merge(self):
        market = self.market()
        client = self.client_type()
        for s in market:
            c = client.get(s.ins_code)
            if c:
                s.buy_count = c["buy_count"]
                s.sell_count = c["sell_count"]
                s.buy_volume = c["buy_volume"]
                s.sell_volume = c["sell_volume"]
            else:
                s.buy_count = 0
                s.sell_count = 0
                s.buy_volume = 0
                s.sell_volume = 0
        return market
