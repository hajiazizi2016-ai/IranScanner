import os
import time
import requests


class TSETMCClient:

    API_BASE = "https://cdn.tsetmc.com/api"
    OLD_BASES = (
        "http://old.tsetmc.com/tsev2/data",
        "https://old.tsetmc.com/tsev2/data",
    )

    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False
        self.tse_proxy = os.getenv("TSE_PROXY", "").strip()
        if self.tse_proxy:
            self.session.proxies.update({"http": self.tse_proxy, "https": self.tse_proxy})
            print("TSETMC client proxy configured")
        else:
            self.session.proxies.clear()
        self.session.headers.update({"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        self.timeout = 30
        self.retry = 2
        print("TSETMC Client initialized")

    def _request(self, url):
        last_error = None
        for attempt in range(self.retry):
            try:
                r = self.session.get(url, timeout=self.timeout)
                r.raise_for_status()
                return r
            except requests.RequestException as exc:
                last_error = exc
                if attempt < self.retry - 1:
                    time.sleep(1 + attempt)
        raise last_error

    def get(self, api):
        return self._request(self.API_BASE + api).json()

    def get_old(self, path):
        last_error = None
        for base in self.OLD_BASES:
            try:
                return self._request(base + path).text
            except requests.RequestException as exc:
                last_error = exc
        raise last_error
