import requests
from pprint import pprint

# 画像のファイル名（「File:foo.jpg」の形で）
file_string = "File:Billy_Tipton.jpg"

# MediaWiki APIのURL（エンドポイント）
url_api = "https://en.wikipedia.org/w/api.php"

# APIのパラメータ
params = {
    "action": "query",
    "format": "json",
    "prop": "imageinfo",
    "iiprop": "url",
    "titles": file_string
}

# JSONデータを取得
session = requests.Session()
response = session.get(url=url_api, params=params)
data = response.json()

# データを絞る
pages = data['query']['pages']
page = list(pages.values())

# 画像のURLを取得
url_image = page[0]['imageinfo'][0]['url']

print(url_image)