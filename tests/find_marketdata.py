import requests
import re

url = "https://www.tsetmc.com/main.926ae21b77b1fef6cf15.js"

text = requests.get(url).text

for x in re.findall(r'.{0,200}getMarketDataAll.{0,400}', text):
    print("\n----------------\n")
    print(x)