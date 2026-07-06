import requests

url = "https://www.tsetmc.com/tsev2/data/instinfofast.aspx?i=46348559193224090&c=57"

response = requests.get(url)

print(response.text)