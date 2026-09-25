import json
import os


class AdaptiveScore:

    FILE = "config/weights.json"

    DEFAULT = {

        "buyer_power": 30,

        "money_flow": 20,

        "volume": 20,

        "rr": 20,

        "support": 10

    }

    def __init__(self):

        os.makedirs("config", exist_ok=True)

        if not os.path.exists(self.FILE):

            with open(self.FILE, "w") as f:

                json.dump(self.DEFAULT, f, indent=4)

        self.load()

        print("Adaptive Score initialized")

    def load(self):

        with open(self.FILE, "r") as f:

            self.weight = json.load(f)

    def save(self):

        with open(self.FILE, "w") as f:

            json.dump(self.weight, f, indent=4)

    def score(self, s):

        score = 0

        score += min(s.buyer_power * self.weight["buyer_power"], 30)

        score += min(s.money_flow_power * self.weight["money_flow"], 20)

        score += min(s.volume_ratio * self.weight["volume"], 20)

        score += min(s.rr * self.weight["rr"], 20)

        score += min(s.rr_power * self.weight["support"], 10)

        return round(score, 2)

    def learn(self, trades):

        if len(trades) == 0:

            return

        avg = sum(x["profit"] for x in trades) / len(trades)

        if avg > 8:

            self.weight["buyer_power"] += 1

            self.weight["money_flow"] += 1

        elif avg < 2:

            self.weight["volume"] += 1

            self.weight["support"] += 1

        total = sum(self.weight.values())

        for k in self.weight:

            self.weight[k] = round(

                self.weight[k] * 100 / total,

                2

            )

        self.save()


