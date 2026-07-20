from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from core.client_type_history_downloader import ClientTypeHistoryDownloader


class HistoryEngine:

    def __init__(self, downloader):

        self.downloader = downloader

        self.client_type_downloader = ClientTypeHistoryDownloader()

        print("History Engine initialized")

    def download_symbol(self, symbol):

        try:

            history = self.downloader.download(symbol.ins_code)

            symbol.history = history

        except Exception:

            symbol.history = []

        try:

            symbol.client_history = self.client_type_downloader.download(
                symbol.ins_code
            )

        except Exception:

            symbol.client_history = []

        return symbol

    def download_all(

        self,

        symbols,

        workers=12

    ):

        result = []

        total = len(symbols)

        finished = 0

        with ThreadPoolExecutor(

            max_workers=workers

        ) as executor:

            futures = {
                executor.submit(
                    self.download_symbol,
                    sym
                 ): sym
                for sym in symbols
            }

            for future in as_completed(futures):

                finished += 1

                if finished % 100 == 0:

                    print(

                        f"History {finished}/{total}"

                    )

                result.append(

                    future.result()

                )

        return result

    def attach_client_type(

        self,

        symbols,

        client_map

    ):

        for s in symbols:

            c = client_map.get(

                s.ins_code

            )

            if c:

                s.buy_count = c["buy_count"]

                s.sell_count = c["sell_count"]

                s.buy_volume = c["buy_volume"]

                s.sell_volume = c["sell_volume"]

            else:

                s.buy_count = 0

                s.sell_count = 0

                s.buy_volume = 0

                s.sell_volume = 0

        return symbols

    def prepare(

        self,

        symbols,

        client_map

    ):

        symbols = self.download_all(symbols)

        symbols = self.attach_client_type(

            symbols,

            client_map

        )

        return symbols


