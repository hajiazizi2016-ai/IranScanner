from core.tsetmc_client import TSETMCClient


class HistoryDownloader:

    def __init__(self):

        self.client = TSETMCClient()

        print("History Downloader initialized")

    def update(self, snapshots):

        for snapshot in snapshots:

            try:

                snapshot.history = self.download(snapshot.ins_code)

            except Exception:

                snapshot.history = []

    def download(self, ins_code):

        raw = self.client.get_old(
            f"/InstTradeHistory.aspx?i={ins_code}&Top=60&A=1"
        )

        history = []

        if not raw:
            return history

        rows = raw.strip().split(";")

        for row in rows:

            fields = row.split("@")

            if len(fields) < 10:
                continue

            try:

                history.append(
                    {
                        "date": fields[0],
                        "high": float(fields[1]),
                        "low": float(fields[2]),
                        "close": float(fields[3]),
                        "last": float(fields[4]),
                        "open": float(fields[5]),
                        "yesterday": float(fields[6]),
                        "value": int(float(fields[7])),
                        "volume": int(float(fields[8])),
                        "count": int(float(fields[9])),
                        "buy_volume": 0,
                        "sell_volume": 0,
                        "buy_count": 0,
                        "sell_count": 0,
                    }
                )

            except Exception as e:

                print("ROW ERROR:", ins_code, e)

                continue

        return history


