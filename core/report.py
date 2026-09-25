import csv
import os


class ReportGenerator:

    def __init__(self):

        os.makedirs("reports", exist_ok=True)

        print("Report Generator initialized")

    def export_scan(self, results):

        file_name = "reports/scan_result.csv"

        with open(

            file_name,

            "w",

            newline="",

            encoding="utf-8-sig"

        ) as f:

            writer = csv.writer(f)

            writer.writerow([

                "Symbol",

                "FinalRank",

                "BuyerPower",

                "VolumeRatio",

                "MoneyFlow",

                "RR",

                "RRPower",

                "SmartMoneyScore",

                "Reason"

            ])

            for s in results:

                writer.writerow([

                    s.symbol,

                    round(s.final_rank,2),

                    round(s.buyer_power,2),

                    round(s.volume_ratio,2),

                    round(s.money_flow_power,2),

                    round(s.rr,2),

                    round(s.rr_power,2),

                    s.smart_money_score,

                    s.smart_money_reason

                ])

        print(file_name)

    def export_backtest(self, report):

        file_name = "reports/backtest.csv"

        with open(

            file_name,

            "w",

            newline="",

            encoding="utf-8-sig"

        ) as f:

            writer = csv.writer(f)

            writer.writerow([

                "InsCode",

                "ProfitPercent"

            ])

            for r in report:

                writer.writerow([

                    r["ins_code"],

                    r["profit"]

                ])

        print(file_name)


