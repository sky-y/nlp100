# 06. 集合
# “paraparaparadise”と”paragraph”に含まれる文字bi-gramの集合を，それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．さらに，’se’というbi-gramがXおよびYに含まれるかどうかを調べよ．

def bigram(s):
    # 文字bi-gram
    bigram_char = []

    for i in range(len(s) - 1):
        bigram_char.append((s[i], s[i + 1]))
    return bigram_char

s1 = "paraparaparadise"
s2 = "paragraph"

bigram1 = set(bigram(s1))
bigram2 = set(bigram(s2))

print(bigram1)
# [('p', 'a'), ('a', 'r'), ('r', 'a'), ('a', 'p'), ('p', 'a'), ('a', 'r'), ('r', 'a'), ('a', 'p'), ('p', 'a'), ('a', 'r'), ('r', 'a'), ('a', 'd'), ('d', 'i'), ('i', 's'), ('s', 'e')]

print(bigram2)
# [('p', 'a'), ('a', 'r'), ('r', 'a'), ('a', 'g'), ('g', 'r'), ('r', 'a'), ('a', 'p'), ('p', 'h')]

# 和集合
print(bigram1 | bigram2)
# {('a', 'd'), ('s', 'e'), ('a', 'r'), ('r', 'a'), ('i', 's'), ('d', 'i'), ('p', 'a'), ('g', 'r'), ('p', 'h'), ('a', 'g'), ('a', 'p')}

# 積集合
print(bigram1 & bigram2)
# {('a', 'p'), ('p', 'a'), ('a', 'r'), ('r', 'a')}

# 差集合
print(bigram1 - bigram2)
# {('a', 'd'), ('s', 'e'), ('i', 's'), ('d', 'i')}

# 含む
print(('s', 'e') in bigram1)
# True
print(('s', 'e') in bigram2)
# False

