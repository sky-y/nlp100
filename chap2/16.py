# 16. ファイルをN分割する
# 自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．同様の処理をsplitコマンドで実現せよ．

import sys
import math

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

# 注意：コマンドライン引数は文字列なので、整数に変換する
n = int(sys.argv[1])

# 行数の計算
print(len(list_input))
# 2780
print(len(list_input) // n)
# n = 3の場合: 926

# 出力させたい行の幅の計算
print(0, (len(list_input) // n) * 1 - 1)
print((len(list_input) // n) * 1, (len(list_input) // n) * 2 - 1)
print((len(list_input) // n) * 2, len(list_input) - 1)

# 正確に行うために、小数の割り算を行い、小数点以下をmath.ceilで切り上げる
len_split = math.ceil(len(list_input) / n)
# len_split = len(list_input) // n

# ファイル名を「python-split-00」のようにしたい
# →回数をカウントしておく
times = 0

for i in range(0, len(list_input), len_split):
    # ファイル名を「python-split-00」のようにしたい
    output_name = f"python-split-{times:02}"
    print(output_name)

    print("[", i, ":", i + len_split, "]")

    # ファイルの書き出し
    with open(output_name, mode="w") as f:
        # 書き出し対象のリスト
        list_output = list_input[i:i+len_split]

        # リストをファイルに書き出す
        f.writelines(list_output)
    
    # print("".join(list_input[i:i+len_split-1]))

    times += 1


# コマンド
# 注意：BSDのsplitには -n や -d オプションがない（GNUのみ）
# → brew install coreutils
# 参考 https://linuxjm.osdn.jp/info/GNU_coreutils/coreutils-ja_31.html
#     https://yu8mada.com/2018/07/25/install-gnu-commands-on-macos-with-homebrew/
# 
# GNU: split -n l/3 -d popular-names.txt split-
# macOS: gsplit -n l/3 -d popular-names.txt split-
# → split-00, split-01, split-02