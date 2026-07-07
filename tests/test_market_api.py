from core.market_api import MarketAPI
from pprint import pprint

api = MarketAPI()

static_data = api.get_static_data()

print(type(static_data["staticData"]))
print("Count:", len(static_data["staticData"]))

print("\n========== FIRST ITEM ==========\n")

pprint(static_data["staticData"][0])