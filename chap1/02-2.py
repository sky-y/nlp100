# 02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
# 「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．

s1 = "パトカー"
s2 = "タクシー"
s = ""

for i in range(len(s1)):
    s += s1[i] + s2[i]

print(s)
# パタトクカシーー