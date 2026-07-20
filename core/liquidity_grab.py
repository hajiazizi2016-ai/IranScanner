class LiquidityGrabDetector:

    def __init__(self):

        print("Liquidity Grab Detector initialized")

    def detect(self, s):

        history = s.history

        s.liquidity_grab = False

        s.fake_breakout = False

        s.stop_hunt = False

        if history is None:

            return s

        if len(history) < 20:

            return s

        today = history[0]

        yesterday = history[1]

        high20 = max(float(x["high"]) for x in history[1:20])

        low20 = min(float(x["low"]) for x in history[1:20])

        close = float(today["close"])

        high = float(today["high"])

        low = float(today["low"])

        prev_close = float(yesterday["close"])

        # شکار نقدینگی بالا

        if high > high20 and close < high20:

            s.liquidity_grab = True

            s.fake_breakout = True

        # شکار نقدینگی پایین

        elif low < low20 and close > low20:

            s.liquidity_grab = True

            s.stop_hunt = True

        # شکست ناموفق

        if abs(close - prev_close) < (prev_close * 0.002):

            s.fake_breakout = True

        return s


