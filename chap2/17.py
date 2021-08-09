# 17. １列目の文字列の異なり
# 1列目の文字列の種類（異なる文字列の集合）を求めよ．確認にはcut, sort, uniqコマンドを用いよ．

path_input = "./popular-names.txt"

## 12.pyのコードを流用する（1列目）

list1 = []

with open(path_input) as f:
    list_input = f.readlines()

for line in list_input:
    list_split1 = line.split("\t")
    list1.append(list_split1[0] + "\n")

# リストから集合に変換することで、重複を排除する
# 注意：setは順序を保証しないため、先に集合を作ってからソートする
set1 = set(list1)

# 集合をソートする
list1_sorted = sorted(list(set1))

print("".join(list1_sorted))

# コマンド
# cut -f 1 popular-names.txt | sort | uniq > col1_sort_uniq.txt
