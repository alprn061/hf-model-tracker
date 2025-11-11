import requests, json

URL = "https://huggingface.co/api/models?sort=lastModified&limit=5"
resp = requests.get(URL, timeout=30)
resp.raise_for_status()
data = resp.json()

# örnek: ilk kaydın temel alanlarını yazdır
first = data[0] if data else {}
print(json.dumps({
    "modelId": first.get("modelId"),
    "pipeline_tag": first.get("pipeline_tag"),
    "library_name": first.get("library_name"),
    "likes": first.get("likes"),
    "downloads": first.get("downloads"),
    "lastModified": first.get("lastModified"),
    "tags": first.get("tags"),
    "author": first.get("author"),
    "has_config": "config" in first,
    "has_cardData": "cardData" in first
}, indent=2, ensure_ascii=False))

# istersen tüm alanları görmek için (gürültülü olabilir):
# print(json.dumps(first, indent=2, ensure_ascii=False))
