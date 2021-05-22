# 05. n-gram
# 与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ．この関数を用い，”I am an NLPer”という文から単語bi-gram，文字bi-gramを得よ．

s = "I am an NLPer"
words = s.split(" ")

# 単語bi-gram
bigram_word = []

for i in range(len(words) - 1):
    bigram_word.append((words[i], words[i + 1]))

print(bigram_word)

# 文字bi-gram
bigram_char = []

for i in range(len(s) - 1):
    bigram_char.append((s[i], s[i + 1]))

print(bigram_char)
# [('I', 'am'), ('am', 'an'), ('an', 'NLPer')]
# [('I', ' '), (' ', 'a'), ('a', 'm'), ('m', ' '), (' ', 'a'), ('a', 'n'), ('n', ' '), (' ', 'N'), ('N', 'L'), ('L', 'P'), ('P', 'e'), ('e', 'r')]
