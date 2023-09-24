import requests

url = "https://dev.laurentiumarian.ro/scraper/Scrapers_start_with_digi/"

r = requests.post(url, data = {"update": "true"})

response = r.json()

if response.get("succes"):
    print(response.get("succes"))
else:
    print(response.get("error"))