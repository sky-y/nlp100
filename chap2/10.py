# 10. 行数のカウント
# 行数をカウントせよ．確認にはwcコマンドを用いよ．

path_input = "./popular-names.txt"

with open(path_input) as f:
    print(len(list(f)))

# $ wc -l popular-names.txt 
#     2780 popular-names.txt