# 20. JSONデータの読み込み
# Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．問題21-29では，ここで抽出した記事本文に対して実行せよ．

import gzip
import json

# デバッグ用
from pprint import *
import pdb


input_file = "./jawiki-country.json.gz"

# gzのままで扱える
# mode="rt": 読み込み "r" + テキストモード "t"
# encoding="utf-8": 文字コード指定
#   ないと「BrokenPipeError: [Errno 32] Broken pipe」になる
with gzip.open(input_file, mode="rt", encoding="utf-8") as f:
    # 今回のファイルはJSONが複数つながった形（厳密な意味でのJSONではない）ため、
    # 1行ごとバラす必要がある
    for line in f:
        # line の中身を出力する
        # print(line)

        # デバッグ：ターミナル上で
        # pdb.set_trace()

        # json.loads: 文字列を解釈
        # json.load: ストリーム（IO）を解釈
        data_line = json.loads(line)

        if data_line["title"] == "イギリス":
            # print(data)
            # print(json.dumps(data_line))
            data = data_line
            break

print(data)

# 結果：title が「イギリス」のJSONデータ（省略）

## 補足：コマンドによるgzファイル展開
## ※ macOS: そのままFinder上でダブルクリック
## ※ Windows: Lhaplusとかで展開
## gunzip -c jawiki-country.json.gz > jawiki-country2.json

