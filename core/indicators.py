from statistics import mean
import math


class Indicators:


    def __init__(self):

        pass


    # ==============================
    # Simple Moving Average
    # ==============================

    def sma(

        self,

        history,

        period

    ):

        if len(history) < period:

            return 0


        values = []


        for row in history[:period]:

            values.append(

                float(row["close"])

            )


        return round(

            sum(values) / period,

            2

        )


    # ==============================
    # Exponential Moving Average
    # ==============================

    def ema(

        self,

        history,

        period

    ):

        if len(history) < period:

            return 0


        prices = []


        for row in reversed(history):

            prices.append(

                float(row["close"])

            )


        multiplier = 2 / (period + 1)


        ema = prices[0]


        for price in prices[1:]:

            ema = (

                price - ema

            ) * multiplier + ema


        return round(

            ema,

            2

        )


    # ==============================
    # Average Volume
    # ==============================

    def vAve(

        self,

        history,

        period

    ):

        if len(history) < period:

            return 0


        volumes = []


        for row in history[:period]:

            volumes.append(

                int(row["volume"])

            )


        return round(

            mean(volumes),

            0

        )


    # ==============================
    # Maximum Volume
    # ==============================

    def vMax(

        self,

        history,

        period

    ):

        if len(history) == 0:

            return 0


        volumes = []


        for row in history[:period]:

            volumes.append(

                int(row["volume"])

            )


        return max(volumes)
    # ==============================
    # Buyer Power
    # ==============================

    def buyer_power(

        self,

        buy_volume,

        buy_count,

        sell_volume,

        sell_count

    ):


        if buy_count == 0:

            return 0


        if sell_count == 0:

            return 0


        buy_avg = buy_volume / buy_count

        sell_avg = sell_volume / sell_count


        if sell_avg == 0:

            return 0


        return round(

            buy_avg / sell_avg,

            2

        )



    # ==============================
    # Money Flow
    # ==============================

    def money_flow(

        self,

        history

    ):


        if len(history) < 2:

            return 0


        total = 0


        for row in history[:20]:


            price = float(row["close"])

            value = float(row["value"])


            total += price * value


        return round(

            total,

            2

        )



    # ==============================
    # Money Flow Power
    # ==============================

    def money_flow_power(

        self,

        history

    ):


        if len(history) < 10:

            return 0


        recent = 0

        old = 0


        for row in history[:5]:

            recent += float(row["value"])


        for row in history[5:10]:

            old += float(row["value"])


        if old == 0:

            return 0


        return round(

            recent / old,

            2

        )



    # ==============================
    # True Range
    # ==============================

    def tr(

        self,

        high,

        low,

        prev_close

    ):


        return max(

            high - low,

            abs(high - prev_close),

            abs(low - prev_close)

        )
    # ==============================
    # ATR
    # ==============================

    def atr(

        self,

        history,

        period=14

    ):


        if len(history) < period + 1:

            return 0


        values = []


        for i in range(period):


            high = float(history[i]["high"])

            low = float(history[i]["low"])

            prev_close = float(history[i + 1]["close"])


            values.append(

                self.tr(

                    high,

                    low,

                    prev_close

                )

            )


        return round(

            mean(values),

            2

        )



    # ==============================
    # VWAP
    # ==============================

    def vwap(

        self,

        history

    ):


        if len(history) == 0:

            return 0


        pv = 0

        volume = 0


        for row in history[:20]:


            close = float(row["close"])

            vol = float(row["volume"])


            pv += close * vol

            volume += vol


        if volume == 0:

            return 0


        return round(

            pv / volume,

            2

        )



    # ==============================
    # RSI
    # ==============================

    def rsi(

        self,

        history,

        period=14

    ):


        if len(history) < period + 1:

            return 0


        gains = []

        losses = []


        for i in range(period):


            current = float(history[i]["close"])

            previous = float(history[i + 1]["close"])


            diff = current - previous


            if diff >= 0:

                gains.append(diff)

                losses.append(0)


            else:

                gains.append(0)

                losses.append(abs(diff))


        avg_gain = mean(gains)

        avg_loss = mean(losses)


        if avg_loss == 0:

            return 100


        rs = avg_gain / avg_loss


        return round(

            100 - (100 / (1 + rs)),

            2

        )



    # ==============================
    # MACD
    # ==============================

    def macd(

        self,

        history

    ):


        if len(history) < 30:

            return 0


        ema12 = self.ema(

            history,

            12

        )


        ema26 = self.ema(

            history,

            26

        )


        return round(

            ema12 - ema26,

            2

        )

    # ==============================
    # ATR Percent
    # ==============================

    def atr_percent(

        self,

        history

    ):


        atr = self.atr(

            history

        )


        if atr == 0:

            return 0


        close = float(

            history[0]["close"]

        )


        if close == 0:

            return 0


        return round(

            atr * 100 / close,

            2

        )



    # ==============================
    # Price Change %
    # ==============================

    def price_change(

        self,

        history

    ):


        if len(history) < 2:

            return 0


        last = float(

            history[0]["close"]

        )


        prev = float(

            history[1]["close"]

        )


        if prev == 0:

            return 0


        return round(

            (last - prev) * 100 / prev,

            2

        )



    # ==============================
    # Average Value
    # ==============================

    def average_value(

        self,

        history,

        period=20

    ):


        if len(history) < period:

            return 0


        values = []


        for row in history[:period]:

            values.append(

                float(row["value"])

            )


        return round(

            mean(values),

            0

        )



    # ==============================
    # Volume Ratio
    # ==============================

    def volume_ratio21(

        self,

        history,

        today_volume

    ):


        avg = self.vAve(

            history,

            21

        )


        if avg == 0:

            return 0


        return round(

            today_volume / avg,

            2

        )



    # ==============================
    # Highest Close
    # ==============================

    def highest_close(

        self,

        history,

        period=60

    ):


        values = []


        for row in history[:period]:

            values.append(

                float(row["close"])

            )


        if len(values) == 0:

            return 0


        return max(values)



    # ==============================
    # Lowest Close
    # ==============================

    def lowest_close(

        self,

        history,

        period=60

    ):


        values = []


        for row in history[:period]:

            values.append(

                float(row["close"])

            )


        if len(values) == 0:

            return 0


        return min(values)
    # ==============================
    # Support
    # ==============================

    def support(

        self,

        history,

        current_price,

        day=60

    ):


        max_volume = 0

        support_price = 0


        limit = min(

            day,

            len(history)

        )


        for row in history[:limit]:


            close = float(row["close"])

            volume = int(row["volume"])


            if close < current_price:


                if volume > max_volume:


                    max_volume = volume

                    support_price = close


        return (

            round(support_price, 2),

            max_volume

        )



    # ==============================
    # Resistance
    # ==============================

    def resistance(

        self,

        history,

        current_price,

        day=60

    ):


        max_volume = 0

        resistance_price = 0


        limit = min(

            day,

            len(history)

        )


        for row in history[:limit]:


            close = float(row["close"])

            volume = int(row["volume"])


            if close > current_price:


                if volume > max_volume:


                    max_volume = volume

                    resistance_price = close


        return (

            round(resistance_price, 2),

            max_volume

        )



    # ==============================
    # Support Distance %
    # ==============================

    def support_percent(

        self,

        current,

        support

    ):


        if support == 0:

            return 0


        return round(

            (1 - support / current) * 100,

            2

        )



    # ==============================
    # Resistance Distance %
    # ==============================

    def resistance_percent(

        self,

        current,

        resistance

    ):


        if resistance == 0:

            return 0


        return round(

            ((resistance / current) - 1) * 100,

            2

        )



    # ==============================
    # Risk Reward
    # ==============================

    def rr(

        self,

        current,

        support,

        resistance

    ):


        if support == 0 or resistance == 0:

            return 0


        risk = (

            1 - support / current

        ) * 100


        reward = (

            resistance / current - 1

        ) * 100


        if risk <= 0:

            return 0


        return round(

            reward / risk,

            2

        )
    # ==============================
    # Risk Reward Power
    # ==============================

    def rr_power(

        self,

        support_volume,

        resistance_volume

    ):

        if resistance_volume == 0:

            return 0


        return round(

            support_volume / resistance_volume,

            2

        )



    # ==============================
    # Maximum History Volume
    # ==============================

    def history_max_volume(

        self,

        history,

        day=60

    ):

        if len(history) == 0:

            return 0


        limit = min(

            day,

            len(history)

        )


        return max(

            int(row["volume"])

            for row in history[:limit]

        )



    # ==============================
    # Volume Peak Ratio
    # ==============================

    def volume_peak_ratio(

        self,

        history,

        day=60

    ):

        vmax = self.history_max_volume(

            history,

            day

        )


        avg = self.vAve(

            history,

            21

        )


        if avg == 0:

            return 0


        return round(

            vmax / avg,

            2

        )



    # ==============================
    # Trend
    # ==============================

    def is_uptrend(

        self,

        history

    ):


        sma20 = self.sma(history, 20)

        sma55 = self.sma(history, 55)


        if sma20 == 0 or sma55 == 0:

            return False


        return sma20 > sma55



    def is_downtrend(

        self,

        history

    ):


        sma20 = self.sma(history, 20)

        sma55 = self.sma(history, 55)


        if sma20 == 0 or sma55 == 0:

            return False


        return sma20 < sma55



    # ==============================
    # Breakout
    # ==============================

    def breakout(

        self,

        current,

        resistance

    ):

        if resistance == 0:

            return False


        return current > resistance



    # ==============================
    # Haghighi Buy Average (میانگین خرید هر حقیقی - میلیون ریال)
    # معادل haghighi_Buy_Ave(ave, delay) در فیلتر اصلی
    # ==============================

    def haghighi_buy_average(
        self,
        client_history,
        price_history,
        period,
        delay=0
    ):

        if len(client_history) < period + delay:
            return 0

        if len(price_history) < period + delay:
            return 0

        total = 0
        count = 0

        for j in range(delay, period + delay):

            c = client_history[j]
            h = price_history[j]

            buy_count = c.get("buy_count", 0)

            if buy_count == 0:
                continue

            per_investor = (
                c.get("buy_volume", 0) / buy_count
            ) * h.get("close", 0)

            total += round(per_investor / 1_000_000, 1)
            count += 1

        if count == 0:
            return 0

        return round(total / period, 2)

    # ==============================
    # KH 3/10 (نسبت خرید هر حقیقی ۳ روز اخیر به ۱۰ روز قبل)
    # معادل kh_3_10 = haghighi_Buy_Ave(3,0) / haghighi_Buy_Ave(10,3)
    # ==============================

    def kh_3_10(
        self,
        client_history,
        price_history
    ):

        recent = self.haghighi_buy_average(
            client_history, price_history, 3, 0
        )

        older = self.haghighi_buy_average(
            client_history, price_history, 10, 3
        )

        if older == 0:
            return 0

        return round(recent / older, 2)

    # ==============================
    # Sarane Average (میانگین قدرت خریدار حقیقی به فروشنده حقیقی)
    # معادل saraneAve(ave, delay) در فیلتر اصلی
    # ==============================

    def sarane_average(
        self,
        client_history,
        period,
        delay=0
    ):

        if len(client_history) < period + delay:
            return 0

        total = 0
        count = 0

        for j in range(delay, period + delay):

            c = client_history[j]

            buy_count = c.get("buy_count", 0)
            sell_count = c.get("sell_count", 0)

            if buy_count == 0 or sell_count == 0:
                continue

            buy_avg = c.get("buy_volume", 0) / buy_count
            sell_avg = c.get("sell_volume", 0) / sell_count

            if sell_avg == 0:
                continue

            total += buy_avg / sell_avg
            count += 1

        if count == 0:
            return 0

        return round(total / period, 2)

    # ==============================
    # Sarane 3/10 (نسبت سرانه خرید ۳ روز اخیر به ۱۰ روز قبل)
    # معادل sarane3_10 = saraneAve(3,0) / saraneAve(10,3)
    # ==============================

    def sarane3_10(
        self,
        client_history
    ):

        recent = self.sarane_average(client_history, 3, 0)
        older = self.sarane_average(client_history, 10, 3)

        if older == 0:
            return 0

        return round(recent / older, 2)

    # ==============================
    # Near Support
    # ==============================

    def near_support(

        self,

        current,

        support,

        percent=3

    ):


        if support == 0:

            return False


        distance = abs(

            current - support

        )


        return (

            distance / current

        ) * 100 <= percent


