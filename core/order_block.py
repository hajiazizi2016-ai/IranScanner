class OrderBlockDetector:

    def __init__(self):

        print("Order Block Detector initialized")

    def detect(self, s):

        history = s.history

        if len(history) < 10:

            s.order_block = False
            s.order_block_price = 0
            return s

        highest = max(float(x["high"]) for x in history[:10])

        lowest = min(float(x["low"]) for x in history[:10])

        last_close = float(history[0]["close"])

        body = abs(float(history[0]["close"]) - float(history[0]["open"]))

        rng = float(history[0]["high"]) - float(history[0]["low"])

        if rng == 0:

            s.order_block = False
            s.order_block_price = 0
            return s

        body_ratio = body / rng

        if body_ratio > 0.6:

            if last_close > highest * 0.995:

                s.order_block = True
                s.order_block_price = highest

            elif last_close < lowest * 1.005:

                s.order_block = True
                s.order_block_price = lowest

            else:

                s.order_block = False
                s.order_block_price = 0

        else:

            s.order_block = False
            s.order_block_price = 0

        return s


