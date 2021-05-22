# 09. Typoglycemia
# スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．ただし，長さが４以下の単語は並び替えないこととする．適当な英語の文（例えば”I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind .”）を与え，その実行結果を確認せよ．

import random

s = "I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind ."

words = s.split(" ")
result = []

for w in words:
    if len(w) > 4:
        l = random.sample(list(w[1:-1]), len(w) - 2)
        result += [w[0] + ''.join(l)  + w[-1]]
        
    else:
        result += [w]

print(" ".join(result))
# I cn’ludot bveleie that I cuold alauctly udansrnted what I was raeidng : the pmoanheenl power of the hmaun mind .
