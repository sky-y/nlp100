# 22. カテゴリ名の抽出
# 記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．

import gzip
import json

import re

# デバッグ用
from pprint import *

# 20.py のJSONファイル読み込みを関数化
def load_json_gz(input_file):

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

# ファイルの読み込み
input_file = "./jawiki-country.json.gz"
data = load_json_gz(input_file)

# データを絞る
data_str = data["text"]

# カテゴリ行を抽出する
pattern_str = r"\[\[Category.+\]\]"
for m in re.finditer(pattern_str, data_str,re.MULTILINE):
    # [[Category:イギリス|*]] の形式
    str_category = m.group()

    # 「イギリス」の部分を絞る
    pattern_str2 = r"\[\[Category:(.+?)(\|.+)?\]\]"
    m2 = re.match(pattern_str2, str_category)
    
    # グループ化されている部分のうち最初（「イギリス」）を抽出
    str_category_name = m2.groups()[0]
    print(str_category_name)

# 結果

# イギリス
# イギリス連邦加盟国
# 英連邦王国
# G8加盟国
# 欧州連合加盟国
# 海洋国家
# 現存する君主国
# 島国
# 1801年に成立した国家・領域