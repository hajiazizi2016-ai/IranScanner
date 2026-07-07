import requests


url = "https://cdn.tsetmc.com/api/MarketData/GetMarketOverview/0"


r = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tsetmc.com",
        "Referer": "https://www.tsetmc.com/"
    },
    timeout=20
)


print("STATUS:")
print(r.status_code)

print("\nTYPE:")
print(r.headers.get("content-type"))

print("\nDATA:")
print(r.text[:2000])