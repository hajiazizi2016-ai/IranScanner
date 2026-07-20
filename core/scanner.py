from core.engine import SmartMoneyEngine
from core.market_api import MarketAPI
from core.history_engine import HistoryEngine
from core.history_downloader import HistoryDownloader
from core.data_provider import DataProvider


class Scanner:

    def __init__(self):

        self.market = MarketAPI()

        self.downloader = HistoryDownloader()

        self.history = HistoryEngine(
            self.downloader
        )

        self.data = DataProvider(
            self.market,
            self.history
        )

        self.engine = SmartMoneyEngine(
            self.data
        )

        print("Scanner initialized V2")

    def scan(self):

        print("Scanning market ...")

        results = self.engine.scan()

        results.sort(
            key=lambda x: (
                getattr(x, "final_rank", 0),
                getattr(x, "smart_money_score", 0),
                getattr(x, "validation_score", 0)
            ),
            reverse=True
        )

        return results

    def print_result(self, results):

        print()
        print("=" * 90)
        print("SMART MONEY RESULTS")
        print("=" * 90)

        if len(results) == 0:
            print("No signal found.")
            return

        print(
            "{:<10}{:<12}{:<8}{:<8}{:<8}{:<8}{:<8}{}".format(
                "Symbol",
                "Score",
                "BP",
                "VOL",
                "FLOW",
                "RR",
                "Power",
                "Reason"
            )
        )

        print("-" * 90)

        for s in results:

            print(
                "{:<10}{:<12}{:<8}{:<8}{:<8}{:<8}{:<8}{}".format(
                    getattr(s, "symbol", ""),
                    round(getattr(s, "final_rank", 0), 2),
                    round(getattr(s, "buyer_power", 0), 2),
                    round(getattr(s, "volume_ratio", 0), 2),
                    round(getattr(s, "money_flow_power", 0), 2),
                    round(getattr(s, "rr", 0), 2),
                    round(getattr(s, "rr_power", 0), 2),
                    getattr(s, "smart_money_reason", "")
                )
            )

    def run(self):

        results = self.scan()

        self.print_result(results)


