# 18. 各行を3コラム目の数値の降順にソート
# 各行を3コラム目の数値の逆順で整列せよ（注意: 各行の内容は変更せずに並び替えよ）．確認にはsortコマンドを用いよ（この問題はコマンドで実行した時の結果と合わなくてもよい）．

# キーとなる値を抽出する関数
# 行 line を与えて、3コラム目（[2]）を取り出したい
# ただし元は文字列なので、整数に変換する必要がある
def mykey(line):
    l = line.split("\t")
    return int(l[2])

path_input = "./popular-names.txt"

with open(path_input) as f:
    lines = f.readlines()

lines_sorted = sorted(lines, key=mykey, reverse=True)

print("".join(lines_sorted))

# コマンド
# sort -r -n -k 3 popular-names.txt > sort-k3.txt