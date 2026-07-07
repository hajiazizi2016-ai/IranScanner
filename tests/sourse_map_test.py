import requests

url = "https://www.tsetmc.com/main.926ae21b77b1fef6cf15.js.map"

r = requests.get(url, timeout=20)

print("STATUS:", r.status_code)
print("TYPE:", r.headers.get("content-type"))
print("LENGTH:", len(r.text))
print(r.text[:200])