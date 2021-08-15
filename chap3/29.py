# 29. 国旗画像のURLを取得する
# テンプレートの内容を利用し，国旗画像のURLを取得せよ．
# （ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）

import gzip
import json

import re
import requests

# デバッグ用
from pprint import *

def load_json_gz(input_file):
    """
    20.py のJSONファイル読み込みを関数化
    """
    # gzのままで扱える
    # mode="rt": 読み込み "r" + テキストモード "t"
    # encoding="utf-8": 文字コード指定
    #   ないと「BrokenPipeError: [Errno 32] Broken pipe」になる
    with gzip.open(input_file, mode="rt", encoding="utf-8") as f:
        # 今回のファイルはJSONが複数つながった形（厳密な意味でのJSONではない）ため、
        # 1行ごとバラす必要がある
        for line in f:
            # json.loads: 文字列を解釈
            data_line = json.loads(line)

            if data_line["title"] == "イギリス":
                return data_line

def extract_body(data_str):
    r"""
    正規表現で文字列を抜き出す：ボディ部分

    {{基礎情報 ...
    }}

    の ... 部分を抜き出す

    >>> extract_body('''{{基礎情報 \nfoo\n}}''')
    'foo'
    """

    # 正規表現パターン
    pattern_body = r'''
        ^\{\{       # 最初の {{
        基礎情報.*?\n # 「基礎情報 国」+改行 ※非貪欲マッチ
        (.*?)       # 任意の文字列（0字以上）※キャプチャ（1番目）
        \n\}\}      # 終端の改行と「}}」
        $           # 文字列の末尾
    '''

    # 正規表現パターンを実行
    # 複数行にマッチさせる（フラグを「re.MULTILINE | re.DOTALL」にセット）
    # パターン文字列内で改行・コメントを入れる（フラグを「re.VERBOSE」にセット）
    re_body = re.search(pattern_body, data_str, re.MULTILINE | re.VERBOSE | re.DOTALL)
    str_body = re_body.group(1)

    return str_body

def extract_key_value(str_body):
    r"""
    正規表現で抜き出したものをリストに格納：キーと値

    >>> extract_key_value("|最大首都 = ロンドン\n")
    [('最大首都', 'ロンドン')]
    """
    pattern_str = r'''
        ^[|]        # 先頭の |
        (.+?)       # キャプチャ(key)、非貪欲
        \s*         # 空白文字0文字以上
        =           # 文字 =
        \s*         # 空白文字0文字以上
        (.+?)       # キャプチャ(value)、非貪欲
        # 以下、キャプチャ対象外（マッチのみ）
        (?:
            (?=\n[|])   # 「改行(\n)と|」の手前までマッチ（肯定の先読み）
            | (?=\n$)     # または「改行(\n)と終端」の手前までマッチ（肯定の先読み）
        )
    '''

    list_found = re.findall(pattern_str, str_body, re.MULTILINE | re.VERBOSE | re.DOTALL)
    return list_found

# ファイルの読み込み
input_file = "./jawiki-country.json.gz"
data = load_json_gz(input_file)

# データを絞る
data_str = data["text"]

# 正規表現で文字列を抜き出す：ボディ部分
str_body = extract_body(data_str)

# 正規表現で抜き出したものをリストに格納：キーと値
list_found = extract_key_value(str_body)

# 辞書に変換
dict_result = dict(list_found)

# 国旗のファイル名を取得
# ただし「File:」を追加する
filename_flag = 'File:' + dict_result['国旗画像']

# MediaWiki APIのURL（エンドポイント）
url_api = "https://en.wikipedia.org/w/api.php"

# APIのパラメータ
params = {
    "action": "query",
    "format": "json",
    "prop": "imageinfo",
    "iiprop": "url",
    "titles": filename_flag
}

# JSONデータを取得
session = requests.Session()
response = session.get(url=url_api, params=params)

if response.status_code != 200:
    print("Error: Status code is not 200")
    exit(1)

data = response.json()

# データを絞る
pages = data['query']['pages']
page = list(pages.values())

# 画像のURLを取得
url_image = page[0]['imageinfo'][0]['url']

print(url_image)