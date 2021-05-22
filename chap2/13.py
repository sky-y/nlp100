# 13. col1.txtとcol2.txtをマージ
# 12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．確認にはpasteコマンドを用いよ．

col1 = "./col1.txt"
col2 = "./col2.txt"

with open(col1) as f1:
    list1 = f1.readlines()

with open(col2) as f2:
    list2 = f2.readlines()

for i in range(len(list1)):
    s = list1[i].rstrip() + "\t" + list2[i].rstrip()
    print(s)

# paste -d "\t" col1.txt col2.txt > merge_paste.txt