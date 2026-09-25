class ClientTypeParser:

    def __init__(self):

        print("ClientType Parser initialized")

    def parse(self, raw):

        result = {}

        if not raw:

            return result

        rows = raw.split(";")

        for row in rows:

            fields = row.split(",")

            if len(fields) < 9:

                continue

            try:

                result[fields[0]] = {

                    "buy_count": int(fields[1]),

                    "sell_count": int(fields[3]),

                    "buy_volume": int(fields[5]),

                    "sell_volume": int(fields[7])

                }

            except Exception:

                continue

        return result


