# 15. 末尾のN行を出力
# 自然数Nをコマンドライン引数などの手段で受け取り，入力のうち末尾のN行だけを表示せよ．確認にはtailコマンドを用いよ．

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

# 標準入力から読み取る場合
# n = input()
# n = int(input())

# # 例：5行分ほしい
# print(len(list_input)) # 2780
# print(len(list_input) - 5) # 2775
# print(len(list_input) - 5 + 1) # 2775

# 注意：ファイルの行番号は1から始まるが、
# リストの添字は0から始まる
line_start = len(list_input) - n

# print(line_start)

for i in range(len(list_input)):
    if i >= line_start:
        print(list_input[i].rstrip())

# tail -n 5 popular-names.txt
