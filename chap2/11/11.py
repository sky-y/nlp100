# 11. タブをスペースに置換
# タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．

# cat popular-names.txt | tr "\t" " "  > popular-names_spaces.txt
# cat popular-names.txt | expand -t 1 > popular-names_spaces2.txt
