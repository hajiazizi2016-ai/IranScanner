class SignalValidator:

    def __init__(self):

        print("Signal Validator initialized")

    def validate(self, s):

        score = 0

        reasons = []

        # ---------------- Buyer Power ----------------

        if s.buyer_power >= 2:

            score += 20

            reasons.append("BuyerPower")

        elif s.buyer_power >= 1.5:

            score += 10

        elif s.buyer_power >= 1.2:

            score += 5

        # ---------------- KH ----------------

        if s.kh_3_10 >= 1.2:

            score += 15

            reasons.append("KH")

        elif s.kh_3_10 >= 1:

            score += 8

        # ---------------- Sarane ----------------

        if s.sarane3_10 >= 1.2:

            score += 10

            reasons.append("Sarane")

        elif s.sarane3_10 >= 1:

            score += 5

        # ---------------- Volume ----------------

        if s.volume_ratio >= 2:

            score += 15

            reasons.append("Volume")

        elif s.volume_ratio >= 1.5:

            score += 10

        elif s.volume_ratio >= 1.2:

            score += 5

        # ---------------- Money Flow ----------------

        if s.money_flow_power >= 1.2:

            score += 15

            reasons.append("MoneyFlow")

        elif s.money_flow_power >= 1:

            score += 8

        # ---------------- RR ----------------

        if s.rr >= 3:

            score += 15

            reasons.append("RR")

        elif s.rr >= 2:

            score += 10

        elif s.rr >= 1.5:

            score += 5

        # ---------------- Support ----------------

        if s.rr_power >= 2:

            score += 10

            reasons.append("Support")

        elif s.rr_power >= 1.5:

            score += 5

        # ---------------- Trend ----------------

        if getattr(s, "uptrend", False):

            score += 5

            reasons.append("Trend")

        # ---------------- Breakout ----------------

        if getattr(s, "breakout", False):

            score += 5

            reasons.append("Breakout")

        # ---------------- Near Support ----------------

        if getattr(s, "near_support", False):

            score += 5

            reasons.append("NearSupport")

        s.validation_score = score

        s.validation_reason = " | ".join(reasons)

        # فقط اینجا تصمیم نهایی

        s.valid_signal = score >= 45

        return s


