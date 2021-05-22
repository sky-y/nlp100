# 08. 暗号文
# 与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．
# ・英小文字ならば(219 - 文字コード)の文字に置換
# ・その他の文字はそのまま出力
# この関数を用い，英語のメッセージを暗号化・復号化せよ

def cipher(s):
    result = ""
    for c in s:
        if str.islower(c):
            result += chr(219 - ord(c))
        else:
            result += c
    return result

s = "I love you."

print(cipher(s))
# I olev blf.

print(cipher(cipher(s)))
# I love you.