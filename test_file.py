import requests
import json

url = "https://careers.hpe.com/widgets"

payload = json.dumps({
  "lang": "en_us",
  "deviceType": "desktop",
  "country": "us",
  "pageName": "search-results",
  "ddoKey": "refineSearch",
  "sortBy": "",
  "subsearch": "",
  "from": 0,
  "jobs": True,
  "counts": True,
  "all_fields": [
    "category",
    "country",
    "state",
    "city",
    "type",
    "postalCode",
    "remote"
  ],
  "size": 10,
  "clearAll": False,
  "jdsource": "facets",
  "isSliderEnable": False,
  "pageId": "page11",
  "siteType": "external",
  "keywords": "",
  "global": True,
  "selected_fields": {
    "country": [
      "Romania"
    ]
  },
  "locationData": {}
})
headers = {
  'content-type': 'application/json',
  'Cookie': 'PHPPPE_ACT=e98745ea-e0b4-443c-b650-49b1427a441b; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiJlOTg3NDVlYS1lMGI0LTQ0M2MtYjY1MC00OWIxNDI3YTQ0MWIifSwibmJmIjoxNzE1NzAyMTkyLCJpYXQiOjE3MTU3MDIxOTJ9.EcWP9UdmlwJEC37CEc6gU1HNiQK76GDk2k4LgeVGfdo'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
print(type(response))
