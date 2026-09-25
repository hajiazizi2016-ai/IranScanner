class SmartMoneyDetector:

    def __init__(self):

        print("Smart Money Detector initialized")

    def detect(self, s):

        score = 0

        reasons = []

        # -----------------------
        # Buyer Power
        # -----------------------

        if s.buyer_power >= 2:

            score += 20

            reasons.append("BuyerPower")

        elif s.buyer_power >= 1.5:

            score += 10

        # -----------------------
        # KH 3/10
        # -----------------------

        if s.kh_3_10 >= 1.2:

            score += 15

            reasons.append("KH3/10")

        # -----------------------
        # Sarane
        # -----------------------

        if s.sarane3_10 >= 1.2:

            score += 10

            reasons.append("Sarane")

        # -----------------------
        # Money Flow
        # -----------------------

        if s.money_flow_power >= 1.2:

            score += 15

            reasons.append("MoneyFlow")

        # -----------------------
        # Volume
        # -----------------------

        if s.volume_ratio >= 2:

            score += 15

            reasons.append("Volume")

        elif s.volume_ratio >= 1.5:

            score += 8

        # -----------------------
        # RR
        # -----------------------

        if s.rr >= 2.5:

            score += 10

            reasons.append("RR")

        # -----------------------
        # Support Power
        # -----------------------

        if s.rr_power >= 2:

            score += 10

            reasons.append("Support")

        # -----------------------
        # Trend
        # -----------------------

        if getattr(s, "uptrend", False):

            score += 5

            reasons.append("Trend")

        # -----------------------
        # Breakout
        # -----------------------

        if getattr(s, "breakout", False):

            score += 5

            reasons.append("Breakout")

        # -----------------------
        # Near Support
        # -----------------------

        if getattr(s, "near_support", False):

            score += 5

            reasons.append("NearSupport")

        s.smart_money_score = score

        s.smart_money_reason = " | ".join(reasons)

        s.smart_money = score >= 60

        return s


