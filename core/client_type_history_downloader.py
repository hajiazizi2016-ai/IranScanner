from core.tsetmc_client import TSETMCClient


class ClientTypeHistoryDownloader:
    """
    دانلود تاریخچه‌ی روزانه‌ی معاملات حقیقی/حقوقی برای یک نماد
    (endpoint: /tsev2/data/clienttype.aspx?i=<InsCode> - 13 ستون)

    ترتیب فیلدها (مشابه ClientTypeAll.aspx که در client_type_parser.py
    استفاده شده - همان الگوی I=Individual/حقیقی, N=Legal/حقوقی):
        0  date
        1  Buy_CountI   (تعداد خریدار حقیقی)
        2  Buy_CountN   (تعداد خریدار حقوقی)
        3  Sell_CountI  (تعداد فروشنده حقیقی)
        4  Sell_CountN  (تعداد فروشنده حقوقی)
        5  Buy_IVolume  (حجم خرید حقیقی)
        6  Buy_NVolume  (حجم خرید حقوقی)
        7  Sell_IVolume (حجم فروش حقیقی)
        8  Sell_NVolume (حجم فروش حقوقی)
        9  Buy_IValue   (ارزش خرید حقیقی)
        10 Buy_NValue   (ارزش خرید حقوقی)
        11 Sell_IValue  (ارزش فروش حقیقی)
        12 Sell_NValue  (ارزش فروش حقوقی)

    فقط ستون‌های مربوط به «حقیقی» (I) استخراج می‌شود، چون فرمول اصلی فیلتر
    (kh_3_10, sarane3_10) روی رفتار خریداران/فروشندگان حقیقی است.
    """

    def __init__(self):

        self.client = TSETMCClient()

        print("ClientType History Downloader initialized")

    def download(self, ins_code):

        raw = self.client.get_old(
            f"/clienttype.aspx?i={ins_code}"
        )

        history = []

        if not raw:
            return history

        rows = raw.strip().split(";")

        for row in rows:

            fields = row.split(",")

            if len(fields) < 9:
                continue

            try:

                history.append(
                    {
                        "date": fields[0],
                        "buy_count": int(float(fields[1] or 0)),
                        "sell_count": int(float(fields[3] or 0)),
                        "buy_volume": int(float(fields[5] or 0)),
                        "sell_volume": int(float(fields[7] or 0)),
                    }
                )

            except Exception:
                continue

        return history
