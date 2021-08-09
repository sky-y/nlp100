# 21. カテゴリ名を含む行を抽出
# 記事中でカテゴリ名を宣言している行を抽出せよ．

import gzip
import json

import re

# デバッグ用
from pprint import *
import pdb

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

input_file = "./jawiki-country.json.gz"
data = load_json_gz(input_file)

data_str = data["text"]

# print(data)
# pprint(data_str)

for m in re.finditer(r"\[\[Category.+\]\]",data_str,re.MULTILINE):
    print(m.group())

# 結果

# [[Category:イギリス|*]]
# [[Category:イギリス連邦加盟国]]
# [[Category:英連邦王国|*]]
# [[Category:G8加盟国]]
# [[Category:欧州連合加盟国|元]]
# [[Category:海洋国家]]
# [[Category:現存する君主国]]
# [[Category:島国]]
# [[Category:1801年に成立した国家・領域]]