class BackTester:

    def __init__(self):

        print("BackTester initialized")


    def run(self, symbols):

        result = {}

        for s in symbols:

            if not hasattr(s, "history"):

                continue


            if len(s.history) < 2:

                continue


            prices = []


            for row in s.history:

                try:

                    date = row.get(
                        "date",
                        ""
                    )

                    close = float(
                        row.get(
                            "close",
                            0
                        )
                    )


                    prices.append(

                        (
                            date,
                            close
                        )

                    )


                except Exception:

                    continue



            if len(prices) > 1:

                result[s.ins_code] = prices



        return result



    def profit(self, prices):

        if len(prices) < 2:

            return 0


        buy = prices[0][1]

        sell = prices[-1][1]


        if buy == 0:

            return 0


        return round(

            ((sell - buy) / buy) * 100,

            2

        )



    def evaluate(self, history):

        report = []


        for ins_code in history:


            p = self.profit(

                history[ins_code]

            )


            report.append(

                {

                    "ins_code": ins_code,

                    "profit": p

                }

            )


        report.sort(

            key=lambda x: x["profit"],

            reverse=True

        )


        return report


