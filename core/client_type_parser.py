class ClientTypeParser:

    def __init__(self):
        print("ClientType Parser initialized")

    @staticmethod
    def _num(value):
        try:
            return int(float(value or 0))
        except (TypeError, ValueError):
            return 0

    def parse(self, raw):
        result = {}
        if not raw:
            return result
        for row in raw.split(";"):
            fields = row.split(",")
            if len(fields) < 9:
                continue
            try:
                result[fields[0]] = {
                    "buy_count": self._num(fields[1]),
                    "sell_count": self._num(fields[3]),
                    "buy_volume": self._num(fields[5]),
                    "sell_volume": self._num(fields[7]),
                }
            except Exception:
                continue
        return result

    def parse_json(self, payload):
        result = {}
        if not isinstance(payload, dict):
            return result
        rows = payload.get("clientTypeAllDto") or payload.get("clientTypeAll") or []
        if isinstance(rows, dict):
            rows = rows.get("clientTypeAllDto") or rows.get("clientTypeAll") or []
        for row in rows:
            if not isinstance(row, dict):
                continue
            ins = str(row.get("insCode") or row.get("instrumentId") or "").strip()
            if not ins:
                continue
            result[ins] = {
                "buy_count": self._num(row.get("buy_CountI") or row.get("buyCountI") or row.get("buy_CountN")),
                "sell_count": self._num(row.get("sell_CountI") or row.get("sellCountI") or row.get("sell_CountN")),
                "buy_volume": self._num(row.get("buy_I_Volume") or row.get("buyIVolume") or row.get("buy_I_Volume")),
                "sell_volume": self._num(row.get("sell_I_Volume") or row.get("sellIVolume") or row.get("sell_I_Volume")),
            }
        return result
