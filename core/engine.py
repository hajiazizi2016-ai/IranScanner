class Engine:

    def __init__(self):
        print("Pro Engine initialized")

    def analyze(self, data):
        print("Analyzing PRO market signals...")

        signals = []

        for item in data:

            if not isinstance(item, dict):
                continue

            symbols = item.get("data", [])

            for s in symbols:

                volume = s.get("volume", 0)
                price = s.get("price", 0)

                # 📊 Relative Volume (فرضی حرفه‌ای‌تر)
                avg_volume = 5000
                rel_volume = volume / avg_volume if avg_volume else 0

                score = 0
                reasons = []

                # 🔥 Smart Money Logic
                if rel_volume > 1:
                    score += 20
                    reasons.append("above average volume")

                if rel_volume > 2:
                    score += 30
                    reasons.append("smart money activity")

                if rel_volume > 4:
                    score += 40
                    reasons.append("strong institutional interest")

                # 📈 Price activity
                if price > 0:
                    score += 10

                final_score = min(score, 100)

                if final_score >= 60:
                    signals.append({
                        "symbol": s["symbol"],
                        "price": price,
                        "volume": volume,
                        "relative_volume": round(rel_volume, 2),
                        "score": final_score,
                        "strength": "STRONG" if final_score >= 80 else "MEDIUM",
                        "reasons": reasons
                    })

        return {
            "count": len(signals),
            "top": sorted(signals, key=lambda x: x["score"], reverse=True)[:10]
        }