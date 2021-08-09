# 19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
# 各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．確認にはcut, uniq, sortコマンドを用いよ．

from pprint import *

path_input = "./popular-names.txt"

## 17.pyのコードを流用する

list1 = []

with open(path_input) as f:
    list_input = f.readlines()

for line in list_input:
    list_split1 = line.split("\t")

    # "\n" は不要なので注意
    list1.append(list_split1[0])

# 集合に変換しない（あとで重複カウントしたいので）

# 集合をソートする
# list1_sorted = sorted(list1)

# カウント用辞書を作る
dict_count = {}
for l in list1:
    if l in dict_count:
        dict_count[l] += 1
    else:
        dict_count[l] = 1

# 辞書の値でソートする
# 注意：結果は [('James', 118), ('William', 111), ...] のようになる
# 適宜 pp 関数でチェックすること
list_count = sorted(dict_count.items(), key=lambda pair: pair[1], reverse=True)

# pp(list_count)

for t in list_count:
    name = t[0]
    count = t[1]
    print(f"{count:4}", name)

# コマンド
# cut -f 1 popular-names.txt | sort | uniq -c | sort -r -k 1 > col1-count-sort.txt