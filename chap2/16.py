# 16. ファイルをN分割する
# 自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．同様の処理をsplitコマンドで実現せよ．

import sys

path_input = "./popular-names.txt"

with open(path_input) as f:
    list_input = f.readlines()
    # 10.pyより、ただし動かない（ファイルオブジェクトの位置が変わるため）
    # len_line = len(list(f))

# コマンドライン引数から受け取る場合
# 引数が足りない場合のエラー（できれば）
if len(sys.argv) < 2:
    print("コマンドライン引数を指定してください。", file=sys.stderr)
    exit(1)

# 注意：input()は文字列を返す
n = int(sys.argv[1])


# コマンド
# 注意：BSDのsplitには -n や -d オプションがない（GNUのみ）
# → brew install coreutils
# 参考 https://linuxjm.osdn.jp/info/GNU_coreutils/coreutils-ja_31.html
#     https://yu8mada.com/2018/07/25/install-gnu-commands-on-macos-with-homebrew/
# 
# GNU: split -n l/3 -d popular-names.txt split-
# macOS: gsplit -n l/3 -d popular-names.txt split-
# → split-00, split-01, split-02