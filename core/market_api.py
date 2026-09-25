import json
import os
import time
import requests

from core.models import SymbolSnapshot
from core.market_parser import MarketParser
from core.client_type_parser import ClientTypeParser


class MarketAPI:

    CDN_BASE = "https://cdn.tsetmc.com/api"
    OLD_BASE = "https://old.tsetmc.com/tsev2/data"

    MARKET_CDN_URL = (
        "/ClosingPrice/GetMarketWatch"
        "?market=0"
        "&paperTypes[0]=1&paperTypes[1]=2&paperTypes[2]=3"
        "&paperTypes[3]=4&paperTypes[4]=5&paperTypes[5]=6"
        "&paperTypes[6]=7&paperTypes[7]=8&paperTypes[8]=9"
        "&withBestLimits=false&hEven=0&RefID=0"
    )
    MARKET_OLD_URL = "/MarketWatchInit.aspx?h=0&r=0"
    CLIENT_CDN_URL = "/ClientType/GetClientTypeAll"
    CLIENT_OLD_URL = "/ClientTypeAll.aspx"

    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False

        proxy = os.getenv("TSE_PROXY", "").strip()
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})
            print("TSETMC proxy configured")
        else:
            self.session.proxies.clear()

        self.market_parser = MarketParser()
        self.client_parser = ClientTypeParser()
        self.market_cache = None
        self.client_cache = None
        self.market_time = 0
        self.client_time = 0
        self.timeout = 20
        self.retry = 2
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
            "Accept": "application/json,text/plain,*/*",
            "Connection": "close",
        }
        print("Market API initialized")

    def _request(self, url, json_expected=False):
        last_error = None
        for attempt in range(self.retry):
            try:
                response = self.session.get(url, timeout=self.timeout, headers=self.headers)
                response.raise_for_status()
                if json_expected:
                    return response.json()
                return response.text
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                if attempt < self.retry - 1:
                    time.sleep(1 + attempt)
        raise last_error

    @staticmethod
    def _num(value, default=0.0):
        try:
            if value in (None, "", "-"):
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

    def _parse_cdn_market(self, payload):
        rows = payload.get("marketwatch", []) if isinstance(payload, dict) else []
        snapshots = []

        for row in rows or []:
            if not isinstance(row, dict):
                continue
            instrument = row.get("instrument") or {}
            ins_code = str(row.get("insCode") or instrument.get("insCode") or "").strip()
            if not ins_code:
                continue

            symbol = str(row.get("lVal18AFC") or instrument.get("lVal18AFC") or instrument.get("lVal18") or "").strip()
            name = str(row.get("lVal30") or instrument.get("lVal30") or "").strip()
            isin = str(row.get("cIsin") or instrument.get("cIsin") or "").strip()

            snapshots.append(SymbolSnapshot(
                ins_code=ins_code,
                isin=isin,
                symbol=symbol,
                name=name,
                market=int(self._num(row.get("flow") or instrument.get("flow"), 0)),
                sector=int(self._num((row.get("sector") or {}).get("cSecVal") if isinstance(row.get("sector"), dict) else 0, 0)),
                close=self._num(row.get("pClosing") or row.get("pc")),
                last=self._num(row.get("pDrCotVal") or row.get("pl")),
                first=self._num(row.get("priceFirst") or row.get("pf")),
                yesterday=self._num(row.get("priceYesterday") or row.get("py")),
                high=self._num(row.get("priceMax") or row.get("pmax")),
                low=self._num(row.get("priceMin") or row.get("pmin")),
                volume=int(self._num(row.get("qTotTran5J"))),
                value=int(self._num(row.get("qTotCap"))),
                count=int(self._num(row.get("zTotTran"))),
            ))

        return snapshots

    def market(self):
        if self.market_cache is not None and time.time() - self.market_time < 5:
            return self.market_cache

        # Primary: modern CDN JSON endpoint. It avoids the old host that
        # is timing out from GitHub-hosted runners.
        try:
            payload = self._request(self.CDN_BASE + self.MARKET_CDN_URL, json_expected=True)
            snapshots = self._parse_cdn_market(payload)
            if snapshots:
                self.market_cache = snapshots
                self.market_time = time.time()
                print(f"Market CDN loaded: {len(snapshots)} symbols")
                return snapshots
            print("Market CDN returned no symbols; trying legacy endpoint")
        except Exception as exc:
            print(f"Market CDN failed: {type(exc).__name__}: {exc}")

        # Secondary: legacy endpoint, kept as a compatibility fallback.
        raw = self._request(self.OLD_BASE + self.MARKET_OLD_URL)
        snapshots = self.market_parser.parse(raw)
        if not snapshots:
            raise RuntimeError("TSETMC market data returned no symbols from CDN or legacy endpoint")
        self.market_cache = snapshots
        self.market_time = time.time()
        return snapshots

    def client_type(self):
        if self.client_cache is not None and time.time() - self.client_time < 10:
            return self.client_cache

        try:
            payload = self._request(self.CDN_BASE + self.CLIENT_CDN_URL, json_expected=True)
            client_map = self.client_parser.parse_json(payload)
            if client_map:
                self.client_cache = client_map
                self.client_time = time.time()
                print(f"Client type CDN loaded: {len(client_map)} symbols")
                return client_map
            print("Client type CDN returned no data; trying legacy endpoint")
        except Exception as exc:
            print(f"Client type CDN failed: {type(exc).__name__}: {exc}")

        raw = self._request(self.OLD_BASE + self.CLIENT_OLD_URL)
        client_map = self.client_parser.parse(raw)
        self.client_cache = client_map
        self.client_time = time.time()
        return client_map

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
        return market
