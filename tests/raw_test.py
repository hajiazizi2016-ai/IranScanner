import requests


url = "https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch"

params = {
    "market": "0"
}

r = requests.get(
    url,
    params=params,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=15
)

print("URL:")
print(r.url)

print("\nSTATUS:")
print(r.status_code)

print("\nDATA:")
print(r.text[:1000])