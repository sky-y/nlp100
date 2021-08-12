# 26. 強調マークアップの除去
# 25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）
# を除去してテキストに変換せよ
# （参考: マークアップ早見表 https://ja.wikipedia.org/wiki/Help:%E6%97%A9%E8%A6%8B%E8%A1%A8 ）．

# 解法参考（25.）：
# https://qiita.com/FukuharaYohei/items/a0ae7f6548db309b7500

import gzip
import json

import re
from collections import OrderedDict

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

# 正規表現で文字列を抜き出す：ボディ部分
#
# {{基礎情報 ...
# }}
#
# の ... 部分を抜き出す
def extract_body(data_str):
    # 正規表現パターン
    pattern_body = r'''
        ^\{\{       # 最初の {{
        基礎情報.*?\n # 「基礎情報 国」+改行 ※非貪欲マッチ
        (.*?)       # 任意の文字列（0字以上）※キャプチャ（1番目）
        \n\}\}      # 終端の改行と「}}」
        $           # 文字列の末尾
    '''

    # 正規表現パターン1を実行
    # 複数行にマッチさせる（フラグを「re.MULTILINE | re.DOTALL」にセット）
    # パターン文字列内で改行・コメントを入れる（フラグを「re.VERBOSE」にセット）
    re_body = re.search(pattern_body, data_str, re.MULTILINE | re.VERBOSE | re.DOTALL)
    str_body = re_body.group(1)

    return str_body

# 正規表現で抜き出したものをリストに格納：キーと値
def extract_key_value(str_body):
    # 正規表現パターン
    # キーと値を取得（あとでOrderedDictに入れる）
    # ただし「|」で始まる行のみ
    # 次に「|」で開始する行までは、文字列を連結したい
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

# print(str_body)

# 正規表現で文字列を抜き出す：ボディ部分
str_body = extract_body(data_str)

# 正規表現で抜き出したものをリストに格納：キーと値
list_found = extract_key_value(str_body)

# 辞書に変換
dict_result = dict(list_found)

# 辞書の値を変換：強調マークアップを除去
dict_replaced = {}
for k, v in dict_result.items():
    # print('key: ', k)
    # print('value: ', v)
    dict_replaced[k] = re.sub(r"[']{2,4}(.+?)[']{2,4}", r"\1", v)

pprint(dict_replaced)

# 結果
