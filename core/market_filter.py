class MarketFilter:

    def filter(self, parsed_data):
        print("Filtering REAL market data...")

        if not parsed_data or parsed_data.get("status") != "ok":
            return []

        symbols = parsed_data.get("symbols", [])

        filtered = [
            s for s in symbols
            if s["volume"] > 0 and s["price"] > 0
        ]

        return {
            "total": len(filtered),
            "data": filtered
        }