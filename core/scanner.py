from core.data_fetcher import DataFetcher
from core.parser import Parser
from core.market_filter import MarketFilter
from core.engine import Engine
from core.db import DB
from core.dashboard import Dashboard
from core.smart_money import SmartMoney


class Scanner:

    def __init__(self):
        self.fetcher = DataFetcher()
        self.parser = Parser()
        self.filter = MarketFilter()
        self.engine = Engine()
        self.db = DB()
        self.dashboard = Dashboard()
        self.smart_money = SmartMoney()

        print("Pro Scanner initialized")


    def run(self):

        print("Scanner started")

        # دریافت داده واقعی
        raw = self.fetcher.get_market_watch()

        # تبدیل داده خام
        parsed = self.parser.parse(raw)

        # فیلتر اولیه
        filtered = self.filter.filter(parsed)


        # تحلیل پول هوشمند
        smart_signals = self.smart_money.analyze(
            filtered.get("data", [])
        )

        print("SMART MONEY SIGNALS:")
        print(smart_signals)


        # تحلیل اصلی Engine
        result = self.engine.analyze(
            [filtered]
        )


        # ذخیره سیگنال‌ها
        self.db.save_signals(
            result.get("top", [])
        )


        # ساخت داشبورد
        dashboard = self.dashboard.build(
            result.get("top", [])
        )


        print("FINAL PRO DASHBOARD:")
        print(dashboard)