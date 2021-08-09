# 23. セクション構造
# 記事中に含まれるセクション名とそのレベル（例えば”== セクション名 ==”なら1）を表示せよ．

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

# pprint(data)

# データを絞る
data_str = data["text"]

# セクション行を抽出する
pattern_str = r"^(=+)(.+?)(=+)"
for m in re.finditer(pattern_str, data_str,re.MULTILINE):
    # [[Category:イギリス|*]] の形式
    str_equals, str_name, _ = m.groups()
    print("セクション名: ", str_name)
    print("レベル: ", str_equals.count('='))
    print()

# 結果

# セクション名:  国名
# レベル:  2
#
# セクション名:  歴史
# レベル:  2
#
# セクション名:  地理
# レベル:  2
#
# セクション名:  主要都市
# レベル:  3
#
# セクション名:  気候
# レベル:  3
#
# セクション名:  政治
# レベル:  2
#
# セクション名:  元首
# レベル:  3
# （以下略）
