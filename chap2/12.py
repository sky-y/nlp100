# 12. 1列目をcol1.txtに，2列目をcol2.txtに保存
# 各行の1列目だけを抜き出したものをcol1.txtに，2列目だけを抜き出したものをcol2.txtとしてファイルに保存せよ．確認にはcutコマンドを用いよ．

path_input = "./popular-names.txt"

col1 = "./col1.txt"
col2 = "./col2.txt"

list1 = []
list2 = []

with open(path_input) as f:
    list_input = f.readlines()

# 1列目

for line in list_input:
    list_split1 = line.split("\t")
    list1.append(list_split1[0] + "\n")

with open(col1, mode="w") as f1:
    f1.writelines(list1)

# 2列目

for line in list_input:
    list_split2 = line.split("\t")
    list2.append(list_split2[1] + "\n")

with open(col2, mode="w") as f2:
    f2.writelines(list2)

# cut -f 1 popular-names.txt > col1_cut.txt
# cut -f 2 popular-names.txt > col2_cut.txt
