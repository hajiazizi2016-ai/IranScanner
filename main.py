from core.scanner import Scanner
from core.backtest import BackTester
from core.report import ReportGenerator


def main():

    scanner = Scanner()

    results = scanner.scan()

    scanner.print_result(results)

    bt = BackTester()

    history = bt.run(
    scanner.engine.data.pipeline()
)

    report = bt.evaluate(history)

    print()

    print("=" * 80)

    print("BACKTEST")

    print("=" * 80)

    for r in report[:20]:

        print(

            r["ins_code"],

            r["profit"]

        )

    reporter = ReportGenerator()

    reporter.export_scan(results)

    reporter.export_backtest(report)


if __name__ == "__main__":

    main()


