import sched

from core.indicators import Indicators
from core.smart_money import SmartMoneyDetector
from core.signal_validator import SignalValidator
from core.ranking import RankingEngine
from core.order_block import OrderBlockDetector
from core.liquidity_grab import LiquidityGrabDetector


class SmartMoneyEngine:

    def __init__(self, data_provider):

        self.data = data_provider

        self.indicators = Indicators()

        self.detector = SmartMoneyDetector()

        self.validator = SignalValidator()

        self.ranking = RankingEngine()

        self.order_block = OrderBlockDetector()

        self.liquidity = LiquidityGrabDetector()

        print(
            "Smart Money Engine V2 initialized"
        )


    # ==========================================
    # Prepare Symbol
    # ==========================================

    def prepare_symbol(self, s):

        try:

            if not hasattr(s, "history"):
                print("NO HISTORY:", getattr(s, "symbol", "?"))
                return None

            if len(s.history) < 60:
                print(
                   "SHORT HISTORY:",
                   getattr(s, "symbol", "?"),
                   len(s.history)
                )  
                print(
                "SHORT HISTORY:",
                getattr(s, "symbol", "?"),
                len(s.history)
            )
                return None

            if not hasattr(s, "client_history"):
                s.client_history = []

            # -----------------------------
            # Volume
            # -----------------------------

            s.avg_volume = self.indicators.vAve(
                s.history,
                21
            )

            s.max_volume = self.indicators.history_max_volume(
                s.history,
                60
            )

            if s.avg_volume > 0:
                s.volume_ratio = round(
                    s.volume / s.avg_volume,
                    2
                )
            else:
                s.volume_ratio = 0

            s.volume_peak_ratio = self.indicators.volume_peak_ratio(
                s.history
            )

            # -----------------------------
            # Moving Average
            # -----------------------------

            s.sma20 = self.indicators.sma(
                s.history,
                20
            )

            s.sma55 = self.indicators.sma(
                s.history,
                55
            )

            # -----------------------------
            # Trend
            # -----------------------------

            s.uptrend = self.indicators.is_uptrend(
                s.history
            )

            s.downtrend = self.indicators.is_downtrend(
                s.history
            )

            # -----------------------------
            # Money Flow
            # -----------------------------

            s.money_flow = self.indicators.money_flow(
                s.history
            )

            s.money_flow_power = self.indicators.money_flow_power(
                s.history
            )

            # -----------------------------
            # Client Type
            # -----------------------------

            s.buyer_power = self.indicators.buyer_power(
                s.buy_volume,
                s.buy_count,
                s.sell_volume,
                s.sell_count
            )

            s.kh_3_10 = self.indicators.kh_3_10(
                s.client_history,
                s.history
            )

            s.sarane3_10 = self.indicators.sarane3_10(
                s.client_history
            )

            s.haghighi_buy_average = self.indicators.haghighi_buy_average(
                s.client_history,
                s.history,
                10
            )

            s.sarane_average = self.indicators.sarane_average(
                s.client_history,
                10
            )

            # -----------------------------
            # Support / Resistance
            # -----------------------------

            s.support, s.support_volume = self.indicators.support(
                s.history,
                s.close,
                60
            )

            s.resistance, s.resistance_volume = self.indicators.resistance(
                s.history,
                s.close,
                60
            )

            # -----------------------------
            # Risk Reward
            # -----------------------------

            s.rr = self.indicators.rr(
                s.close,
                s.support,
                s.resistance
            )

            s.rr_power = self.indicators.rr_power(
                s.support_volume,
                s.resistance_volume
            )

            # -----------------------------
            # Price Position
            # -----------------------------

            s.support_percent = self.indicators.support_percent(
                s.close,
                s.support
            )

            s.resistance_percent = self.indicators.resistance_percent(
                s.close,
                s.resistance
            )

            # -----------------------------
            # Volume Filter
            # -----------------------------

            s.unusual_volume = (
                s.volume_ratio >= 2
            )

            s.volume_breakout = (
                s.volume_peak_ratio >= 1.5
            )

            # -----------------------------
            # Breakout / Support
            # -----------------------------

            s.breakout = self.indicators.breakout(
                s.close,
                s.resistance
            )

            s.near_support = self.indicators.near_support(
                s.close,
                s.support
            )

            # -----------------------------
            # Order Block
            # -----------------------------

            s = self.order_block.detect(
                s
            )

            # -----------------------------
            # Liquidity Grab
            # -----------------------------

            s = self.liquidity.detect(
                s
            )

            # -----------------------------
            # Smart Money Detection
            # -----------------------------

            s = self.detector.detect(
                s
            )

            # -----------------------------
            # Signal Validation
            # -----------------------------

            s = self.validator.validate(
                s
            )

            return s

        except Exception as e:

            print(
                "PREPARE ERROR:",
                getattr(s, "symbol", ""),
                e
            )

            return None  
        
           # ==========================================
           # Scan Market
           # ==========================================
    def scan(self):

        print("Scanning market V2 ...")

        symbols = self.data.pipeline()

        print("TYPE:", type(symbols))
        print("COUNT:", len(symbols))
        print("FIRST:", symbols[:3] if len(symbols) else "EMPTY")

        output = []

        total = len(symbols)

        for index, s in enumerate(symbols, start=1):

            if index <= 3:
                print("PREPARING:", getattr(s, "symbol", "?"))

            item = self.prepare_symbol(s)

            if index <= 3:
                print("RESULT:", item)

            if item is None:
                continue

            output.append(item)

            if index % 250 == 0:
                print(f"Processed {index}/{total}")

        if len(output) == 0:

            print("No prepared symbols.")

            return []

        # ------------------------------------------
        # Ranking
        # ------------------------------------------

        output = self.ranking.calculate(output)

        # ------------------------------------------
        # Diagnostics (تشخیص علت صفر شدن نتایج)
        # ------------------------------------------

        debug_top = sorted(
            output,
            key=lambda x: getattr(x, "validation_score", 0),
            reverse=True
        )[:10]

        print("\n" + "-" * 90)
        print("TOP 10 CANDIDATES (برای تشخیص - حتی اگر رد نشده باشند)")
        print("-" * 90)
        print(
            "{:<10}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<10}{}".format(
                "Symbol", "VScore", "Buyer", "KH", "Sarane",
                "Vol", "RR", "RRPow", "Reason"
            )
        )
        for item in debug_top:
            print(
                "{:<10}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<10}{}".format(
                    getattr(item, "symbol", ""),
                    round(getattr(item, "validation_score", 0), 1),
                    round(getattr(item, "buyer_power", 0), 2),
                    round(getattr(item, "kh_3_10", 0), 2),
                    round(getattr(item, "sarane3_10", 0), 2),
                    round(getattr(item, "volume_ratio", 0), 2),
                    round(getattr(item, "rr", 0), 2),
                    round(getattr(item, "rr_power", 0), 2),
                    getattr(item, "validation_reason", "")
                )
            )
        print("-" * 90 + "\n")

        # ------------------------------------------
        # Final Filter
        # ------------------------------------------

        final = []

        for item in output:

            valid = getattr(
                item,
                "valid_signal",
                False
            )

            score = getattr(
                item,
                "final_score",
                0
            )

            if valid or score >= 60:
                final.append(item)

        print(
            "TOTAL FINAL:",
            len(final)
        )

        return final    # Smart Money Report
    # ==========================================

    def report(self, results):

        print("\n" + "=" * 90)
        print("SMART MONEY RESULTS")
        print("=" * 90)

        if not results:
            print("No signal found.")
            return

        for item in results:

            print("-" * 90)

            print(
                "SYMBOL:",
                getattr(item, "symbol", "")
            )

            print(
                "SCORE:",
                getattr(item, "final_score", 0)
            )

            print(
                "SMART MONEY:",
                getattr(item, "smart_money", False)
            )

            print(
                "VOLUME RATIO:",
                getattr(item, "volume_ratio", 0)
            )

            print(
                "VOLUME PEAK:",
                getattr(item, "volume_peak_ratio", 0)
            )

            print(
                "ORDER BLOCK:",
                getattr(item, "order_block", False)
            )

            print(
                "LIQUIDITY GRAB:",
                getattr(item, "liquidity_grab", False)
            )

            print(
                "BUY POWER:",
                getattr(item, "buyer_power", 0)
            )

    # ==========================================
    # Scan Top Signals
    # ==========================================

    def top_signals(self, limit=20):

        results = self.scan()

        if not results:
            return []

        results = sorted(
            results,
            key=lambda x: getattr(x, "final_score", 0),
            reverse=True
        )

        return results[:limit]    # ==========================================
    # Single Symbol Analysis
    # ==========================================

    def analyze_symbol(self, symbol):

        symbols = self.data.pipeline()

        for s in symbols:

            if getattr(s, "symbol", "") == symbol:

                result = self.prepare_symbol(s)

                if result is not None:
                    return result

        return None


    # ==========================================
    # Debug Symbol
    # ==========================================

    def debug_symbol(self, symbol):

        item = self.analyze_symbol(symbol)

        if item is None:

            print(
                "Symbol not found:",
                symbol
            )

            return None

        print("=" * 70)
        print("DEBUG SYMBOL:", symbol)

        fields = [

            "close",
            "volume_ratio",
            "volume_peak_ratio",
            "smart_money",
            "buyer_power",
            "money_flow",
            "order_block",
            "liquidity_grab",
            "valid_signal",
            "final_score"

        ]

        for field in fields:

            print(
                field,
                ":",
                getattr(item, field, None)
            )

        print("=" * 70)

        return item    # ==========================================
    # Run Scanner
    # ==========================================

    def run(self):

        results = self.scan()

        self.report(results)

        return results


    # ==========================================
    # Export Data
    # ==========================================

    def export_results(self, results):

        data = []

        for item in results:

            row = {

                "symbol": getattr(
                    item,
                    "symbol",
                    ""
                ),

                "score": getattr(
                    item,
                    "final_score",
                    0
                ),

                "volume_ratio": getattr(
                    item,
                    "volume_ratio",
                    0
                ),

                "smart_money": getattr(
                    item,
                    "smart_money",
                    False
                ),

                "buyer_power": getattr(
                    item,
                    "buyer_power",
                    0
                ),

                "order_block": getattr(
                    item,
                    "order_block",
                    False
                ),

                "liquidity_grab": getattr(
                    item,
                    "liquidity_grab",
                    False
                )

            }

            data.append(row)

        return data


    # ==========================================
    # Statistics
    # ==========================================

    def statistics(self, results):

        if not results:

            return {

                "count": 0,
                "average_score": 0

            }

        total_score = 0

        for item in results:

            total_score += getattr(
                item,
                "final_score",
                0
            )

        return {

            "count": len(results),

            "average_score": round(
                total_score / len(results),
                2
            )

        }    # ==========================================
    # Health Check
    # ==========================================

    def health_check(self):

        status = {

            "data_provider":
                self.data is not None,

            "indicators":
                self.indicators is not None,

            "smart_money_detector":
                self.detector is not None,

            "validator":
                self.validator is not None,

            "ranking":
                self.ranking is not None,

            "order_block":
                self.order_block is not None,

            "liquidity":
                self.liquidity is not None

        }

        return status


    # ==========================================
    # Version
    # ==========================================

    def version(self):

        return {

            "engine":
                "SmartMoneyEngine V2",

            "version":
                "2.0",

            "architecture":
                "Smart Money + Order Block + Liquidity + Ranking"

        }


