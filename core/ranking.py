from core.adaptive_score import AdaptiveScore


class RankingEngine:

    def __init__(self):

        self.adaptive = AdaptiveScore()

        print("Ranking Engine initialized")

    def calculate(self, symbols):

        if not symbols:
            return []

        for s in symbols:

            score = self.adaptive.score(s)

            # —Ê‰œ
            if getattr(s, "uptrend", False):
                score += 5

            # ‘ò”  „ﬁ«Ê„ 
            if getattr(s, "breakout", False):
                score += 5

            # ‰“œÌò Õ„«Ì 
            if getattr(s, "near_support", False):
                score += 5

            # ÕÃ„ €Ì—⁄«œÌ
            if getattr(s, "unusual_volume", False):
                score += 5

            # Order Block
            if getattr(s, "order_block", False):
                score += 10

            # ÅÊ· ÂÊ‘„‰œ
            if getattr(s, "smart_money", False):
                score += 10

            # ‰ﬁœ‘Ê‰œêÌ
            if getattr(s, "liquidity_ok", False):
                score += 5

            # «⁄ »«— ”Ìê‰«·
            if getattr(s, "valid_signal", False):
                score += 5

            s.final_rank = round(score, 2)
            s.final_score = round(score, 2)

        symbols.sort(

            key=lambda x: (

                x.final_rank,

                getattr(x, "smart_money_score", 0),

                getattr(x, "validation_score", 0),

                getattr(x, "volume_ratio", 0),

                getattr(x, "money_flow_power", 0),

                getattr(x, "buyer_power", 0)

            ),

            reverse=True

        )

        return symbols

    def top(

        self,

        symbols,

        limit=20

    ):

        ranked = self.calculate(symbols)

        return ranked[:limit]

    def best(self, symbols):

        ranked = self.calculate(symbols)

        if not ranked:
            return None

        return ranked[0]


