from core.models import SymbolSnapshot


class MarketParser:

    def __init__(self):

        print("Market Parser initialized")

    def parse(self, raw):

        snapshots = []

        if not raw:
            return snapshots

        parts = raw.split("@")

        if len(parts) < 3:
            return snapshots

        records = parts[2].split(";")

        for record in records:

            f = record.split(",")

            if len(f) < 23:
                continue

            try:

                s = SymbolSnapshot(

                    ins_code=f[0],

                    isin=f[1],

                    symbol=f[2].strip(),

                    name=f[3].strip(),

                    market=0,

                    sector=0,

                    close=float(f[11] or 0),

                    last=float(f[12] or 0),

                    first=float(f[13] or 0),

                    yesterday=float(f[14] or 0),

                    high=float(f[15] or 0),

                    low=float(f[16] or 0),

                    volume=int(float(f[9] or 0)),

                    value=int(float(f[10] or 0)),

                    count=int(float(f[8] or 0))

                )

                snapshots.append(s)

            except Exception:

                continue

        return snapshots


