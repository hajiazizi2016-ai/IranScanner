class SmartMoney:

    def __init__(self):
        print("Smart Money Engine initialized")

    def analyze(self, symbol_data):

        results = []

        for s in symbol_data:

            volume = s.get("volume", 0)
            price = s.get("price", 0)

            score = 0
            reasons = []

            # حجم بالا
            if volume > 10000:
                score += 30
                reasons.append("high volume")

            # قیمت معتبر
            if price > 0:
                score += 10
                reasons.append("valid price")

            # قدرت اولیه پول هوشمند
            if volume > 50000:
                score += 40
                reasons.append("possible smart money")

            if score >= 50:
                results.append({
                    "symbol": s.get("symbol"),
                    "score": score,
                    "reasons": reasons
                })

        return results