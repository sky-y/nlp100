# 02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
# 「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．

s1 = "パトカー"
s2 = "タクシー"
s = ""

for (c1, c2) in zip(s1, s2):
    s += c1 + c2

print(s)
# パタトクカシーー
