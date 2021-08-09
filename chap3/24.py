# 24. ファイル参照の抽出
# 記事から参照されているメディアファイルをすべて抜き出せ．

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

# print(data_str)

# メディアファイル行を抽出する
pattern_str = r"(\[\[ファイル:(.+?)(\|.+)*\]\]?)"
for m in re.finditer(pattern_str, data_str,re.MULTILINE):
    # ファイル名を抽出
    print(m.groups()[1])

# 結果

# Royal Coat of Arms of the United Kingdom.svg
# United States Navy Band - God Save the Queen.ogg
# Descriptio Prime Tabulae Europae.jpg
# Lenepveu, Jeanne d'Arc au siège d'Orléans.jpg
# London.bankofengland.arp.jpg
# Battle of Waterloo 1815.PNG
# Uk topo en.jpg
# BenNevis2005.jpg
# Population density UK 2011 census.png
# 2019 Greenwich Peninsula & Canary Wharf.jpg
# Leeds CBD at night.jpg
# Palace of Westminster, London - Feb 2007.jpg
# Scotland Parliament Holyrood.jpg
# Donald Trump and Theresa May (33998675310) (cropped).jpg
# Soldiers Trooping the Colour, 16th June 2007.jpg
# City of London skyline from London City Hall - Oct 2008.jpg
# Oil platform in the North SeaPros.jpg
# Eurostar at St Pancras Jan 2008.jpg
# Heathrow Terminal 5C Iwelumo-1.jpg
# UKpop.svg
# Anglospeak.svg
# Royal Aberdeen Children's Hospital.jpg
# CHANDOS3.jpg
# The Fabs.JPG
# Wembley Stadium, illuminated.jpg