import time

from core.history_engine import HistoryEngine


# نام ابزارهایی که «سهام عادی» نیستند و باید از نتایج حذف شوند
# (اختیار معامله، حق تقدم، صندوق‌ها، اوراق، تسهیلات مسکن، آتی، سلف و...)
NON_STOCK_KEYWORDS = [
    "اختيار",
    "اختیار",
    "حق تقدم",
    "صندوق",
    "اوراق",
    "تسهيلات",
    "تسهیلات",
    "آتي",
    "آتی",
    "گواهي سپرده",
    "گواهی سپرده",
    "سلف",
    "خزانه",
]


def is_stock(symbol):

    name = getattr(symbol, "name", "") or ""

    for keyword in NON_STOCK_KEYWORDS:
        if keyword in name:
            return False

    return True


class DataProvider:

    def __init__(
        self,
        market_api,
        history_engine
    ):

        self.market_api = market_api
        self.history_engine = history_engine

        self.cache = None
        self.cache_time = 0
        self.cache_seconds = 900

        print("Data Provider initialized")

    # ==========================================
    # دریافت کل داده بازار
    # ==========================================

    def load_market(self):

        now = time.time()

        if (
            self.cache is not None
            and
            now - self.cache_time < self.cache_seconds
        ):
            return self.cache

        symbols = self.market_api.market()

        before_count = len(symbols)

        symbols = [s for s in symbols if is_stock(s)]

        print(
            "STOCK FILTER: kept",
            len(symbols),
            "of",
            before_count,
            "(non-stock instruments removed)"
        )

        client_map = self.market_api.client_type()

        symbols = self.history_engine.prepare(
            symbols,
            client_map
        )

        self.cache = symbols
        self.cache_time = now

        return symbols

    # ==========================================
    # دریافت نمادها
    # ==========================================

    def symbols(self):

        return self.load_market()

    # ==========================================
    # جستجوی نماد
    # ==========================================

    def get_symbol(
        self,
        ins_code
    ):

        symbols = self.load_market()

        for s in symbols:

            if s.ins_code == ins_code:
                return s

        return None

    # ==========================================
    # حذف داده ناقص
    # ==========================================

    def clean(
        self,
        symbols
    ):

        print("INPUT SYMBOLS:", len(symbols))

        ok = []

        no_history = 0
        none_history = 0
        short_history = 0

        for s in symbols:

            if not hasattr(s, "history"):
                no_history += 1
                continue

            if s.history is None:
                none_history += 1
                continue

            if len(s.history) < 20:
                short_history += 1
                continue

            ok.append(s)

        print("NO HISTORY:", no_history)
        print("NONE HISTORY:", none_history)
        print("SHORT HISTORY:", short_history)
        print("READY:", len(ok))

        return ok
    # ==========================================
    # داده آماده برای تحلیل
    # ==========================================

    def ready(self):

        symbols = self.load_market()

        symbols = self.clean(symbols)

        return symbols

    # ==========================================
    # Refresh دستی
    # ==========================================

    def refresh(self):

        self.cache = None
        self.cache_time = 0

        return self.load_market()

    # ==========================================
    # آمار
    # ==========================================

    def statistics(
        self,
        symbols=None
    ):

        if symbols is None:
            symbols = self.ready()

        return {

            "total": len(symbols),

            "with_history": sum(
                1
                for s in symbols
                if hasattr(s, "history")
                and s.history is not None
                and len(s.history) > 0
            ),

            "avg_history": round(
                (
                    sum(
                        len(s.history)
                        for s in symbols
                        if hasattr(s, "history")
                        and s.history is not None
                    )
                    /
                    max(len(symbols), 1)
                ),
                2
            )

        }

    # ==========================================
    # وضعیت
    # ==========================================

    def health(self):

        return {

            "market_api":
                self.market_api is not None,

            "history_engine":
                self.history_engine is not None,

            "cache":
                self.cache is not None

        }

    # ==========================================
    # خروجی نهایی برای Engine
    # ==========================================

    def pipeline(self):

        return self.ready()

    # ==========================================
    # گزارش
    # ==========================================

    def report(self):

        data = self.statistics()

        print()
        print("=" * 50)
        print("DATA PROVIDER REPORT")
        print("=" * 50)

        for key, value in data.items():
            print(f"{key:20}: {value}")

        print("=" * 50)

        return data


