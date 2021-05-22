# 14. 先頭からN行を出力
# 自然数Nをコマンドライン引数などの手段で受け取り，入力のうち先頭のN行だけを表示せよ．確認にはheadコマンドを用いよ．

path_input = "./popular-names.txt"

with open(path_input) as f:
    list_input = f.readlines()

n = input()

for i in range(int(n)):
    print(list_input[i].rstrip())

# head -n 5 popular-names.txt