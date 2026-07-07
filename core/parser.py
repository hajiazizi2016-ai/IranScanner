class Parser:

    def parse(self, raw_data):
        print("Parsing REAL TSETMC data...")

        if not raw_data or "Error" in raw_data:
            return {
                "status": "error",
                "symbols": []
            }

        rows = raw_data.split("@")
        symbols = []

        for row in rows:
            parts = row.split(";")

            # حداقل داده معتبر
            if len(parts) < 8:
                continue

            try:
                symbol = parts[0]
                last_price = float(parts[2]) if parts[2].isdigit() else 0
                volume = float(parts[6]) if parts[6].isdigit() else 0

                symbols.append({
                    "symbol": symbol,
                    "price": last_price,
                    "volume": volume
                })

            except:
                continue

        return {
            "status": "ok",
            "count": len(symbols),
            "symbols": symbols[:50]
        }