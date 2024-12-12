import requests
import json
response = requests.get("https://0a47koosab.execute-api.ap-southeast-1.amazonaws.com/default/fetchLatestSummary")
summary = response.json()["news"][0]
news = summary["news"]
news_json = json.loads(news)
for new in news_json:
    print(new["title"])
    print(new["summary"])
    print(new["url"])
    print("\n")
