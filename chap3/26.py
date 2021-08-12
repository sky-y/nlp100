# 26. 強調マークアップの除去
# 25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）
# を除去してテキストに変換せよ
# （参考: マークアップ早見表 https://ja.wikipedia.org/wiki/Help:%E6%97%A9%E8%A6%8B%E8%A1%A8 ）．

# 解法参考（25.）：
# https://qiita.com/FukuharaYohei/items/a0ae7f6548db309b7500

import gzip
import json

import re
from collections import OrderedDict

# デバッグ用
from pprint import *

# 20.py のJSONファイル読み込みを関数化
def load_json_gz(input_file):

    # gzのままで扱える
    # mode="rt": 読み込み "r" + テキストモード "t"
    # encoding="utf-8": 文字コード指定
    #   ないと「BrokenPipeError: [Errno 32] Broken pipe」になる
    with gzip.open(input_file, mode="rt", encoding="utf-8") as f:
        # 今回のファイルはJSONが複数つながった形（厳密な意味でのJSONではない）ため、
        # 1行ごとバラす必要がある
        for line in f:
            # json.loads: 文字列を解釈
            data_line = json.loads(line)

            if data_line["title"] == "イギリス":
                return data_line

# 正規表現で文字列を抜き出す：ボディ部分
#
# {{基礎情報 ...
# }}
#
# の ... 部分を抜き出す
def extract_body(data_str):
    # 正規表現パターン
    pattern_body = r'''
        ^\{\{       # 最初の {{
        基礎情報.*?\n # 「基礎情報 国」+改行 ※非貪欲マッチ
        (.*?)       # 任意の文字列（0字以上）※キャプチャ（1番目）
        \n\}\}      # 終端の改行と「}}」
        $           # 文字列の末尾
    '''

    # 正規表現パターン1を実行
    # 複数行にマッチさせる（フラグを「re.MULTILINE | re.DOTALL」にセット）
    # パターン文字列内で改行・コメントを入れる（フラグを「re.VERBOSE」にセット）
    re_body = re.search(pattern_body, data_str, re.MULTILINE | re.VERBOSE | re.DOTALL)
    str_body = re_body.group(1)

    return str_body

# 正規表現で抜き出したものをリストに格納：キーと値
def extract_key_value(str_body):
    # 正規表現パターン
    # キーと値を取得（あとでOrderedDictに入れる）
    # ただし「|」で始まる行のみ
    # 次に「|」で開始する行までは、文字列を連結したい
    pattern_str = r'''
        ^[|]        # 先頭の |
        (.+?)       # キャプチャ(key)、非貪欲
        \s*         # 空白文字0文字以上
        =           # 文字 =
        \s*         # 空白文字0文字以上
        (.+?)       # キャプチャ(value)、非貪欲
        # 以下、キャプチャ対象外（マッチのみ）
        (?:
            (?=\n[|])   # 「改行(\n)と|」の手前までマッチ（肯定の先読み）
            | (?=\n$)     # または「改行(\n)と終端」の手前までマッチ（肯定の先読み）
        )
    '''

    list_found = re.findall(pattern_str, str_body, re.MULTILINE | re.VERBOSE | re.DOTALL)
    return list_found


# ファイルの読み込み
input_file = "./jawiki-country.json.gz"
data = load_json_gz(input_file)

# データを絞る
data_str = data["text"]

# print(str_body)

# 正規表現で文字列を抜き出す：ボディ部分
str_body = extract_body(data_str)

# 正規表現で抜き出したものをリストに格納：キーと値
list_found = extract_key_value(str_body)

# 辞書に変換
dict_result = dict(list_found)

# 辞書の値を変換：強調マークアップを除去
dict_replaced = {}
for k, v in dict_result.items():
    # print('key: ', k)
    # print('value: ', v)
    dict_replaced[k] = re.sub(r"[']{2,4}(.+?)[']{2,4}", r"\1", v)

pprint(dict_replaced)

# 結果

# {'GDP/人': '36,727<ref name="imf-statistics-gdp" />',
#  'GDP値': '2兆3162億<ref name="imf-statistics-gdp" />',
#  'GDP値MER': '2兆4337億<ref name="imf-statistics-gdp" />',
#  'GDP値元': '1兆5478億<ref '
#           'name="imf-statistics-gdp">[http://www.imf.org/external/pubs/ft/weo/2012/02/weodata/weorept.aspx?pr.x=70&pr.y=13&sy=2010&ey=2012&scsm=1&ssd=1&sort=country&ds=.&br=1&c=112&s=NGDP%2CNGDPD%2CPPPGDP%2CPPPPC&grp=0&a=IMF>Data '
#           'and Statistics>World Economic Outlook Databases>By Countrise>United '
#           'Kingdom]</ref>',
#  'GDP統計年': '2012',
#  'GDP統計年MER': '2012',
#  'GDP統計年元': '2012',
#  'GDP順位': '6',
#  'GDP順位MER': '6',
#  'ISO 3166-1': 'GB / GBR',
#  'ccTLD': '[[.uk]] / [[.gb]]<ref>使用は.ukに比べ圧倒的少数。</ref>',
#  '人口値': '6643万5600<ref>{{Cite '
#         'web|url=https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates|title=Population '
#         'estimates - Office for National '
#         'Statistics|accessdate=2019-06-26|date=2019-06-26}}</ref>',
#  '人口大きさ': '1 E7',
#  '人口密度値': '271',
#  '人口統計年': '2018',
#  '人口順位': '22',
#  '他元首等氏名1': '[[:en:Norman Fowler, Baron Fowler|ノーマン・ファウラー]]',
#  '他元首等氏名2': '{{仮リンク|リンゼイ・ホイル|en|Lindsay Hoyle}}',
#  '他元首等氏名3': '[[:en:Brenda Hale, Baroness Hale of Richmond|ブレンダ・ヘイル]]',
#  '他元首等肩書1': '[[貴族院 (イギリス)|貴族院議長]]',
#  '他元首等肩書2': '[[庶民院 (イギリス)|庶民院議長]]',
#  '他元首等肩書3': '[[連合王国最高裁判所|最高裁判所長官]]',
#  '位置画像': 'United Kingdom (+overseas territories) in the World (+Antarctica '
#          'claims).svg',
#  '元首等氏名': '[[エリザベス2世]]',
#  '元首等肩書': '[[イギリスの君主|女王]]',
#  '公式国名': '{{lang|en|United Kingdom of Great Britain and Northern '
#          'Ireland}}<ref>英語以外での正式国名:<br />\n'
#          '*{{lang|gd|An Rìoghachd Aonaichte na Breatainn Mhòr agus Eirinn mu '
#          'Thuath}}（[[スコットランド・ゲール語]]）\n'
#          '*{{lang|cy|Teyrnas Gyfunol Prydain Fawr a Gogledd '
#          'Iwerddon}}（[[ウェールズ語]]）\n'
#          '*{{lang|ga|Ríocht Aontaithe na Breataine Móire agus Tuaisceart na '
#          'hÉireann}}（[[アイルランド語]]）\n'
#          '*{{lang|kw|An Rywvaneth Unys a Vreten Veur hag Iwerdhon '
#          'Glédh}}（[[コーンウォール語]]）\n'
#          '*{{lang|sco|Unitit Kinrick o Great Breetain an Northren '
#          'Ireland}}（[[スコットランド語]]）\n'
#          '**{{lang|sco|Claught Kängrick o Docht Brätain an Norlin '
#          'Airlann}}、{{lang|sco|Unitet Kängdom o Great Brittain an Norlin '
#          'Airlann}}（アルスター・スコットランド語）</ref>',
#  '公用語': '[[英語]]',
#  '国旗画像': 'Flag of the United Kingdom.svg',
#  '国歌': '[[女王陛下万歳|{{lang|en|God Save the Queen}}]]{{en icon}}<br />神よ女王を護り賜え<br '
#        '/>{{center|[[ファイル:United States Navy Band - God Save the Queen.ogg]]}}',
#  '国章リンク': '（[[イギリスの国章|国章]]）',
#  '国章画像': '[[ファイル:Royal Coat of Arms of the United Kingdom.svg|85px|イギリスの国章]]',
#  '国際電話番号': '44',
#  '地図画像': 'Europe-UK.svg',
#  '夏時間': '+1',
#  '建国形態': '建国',
#  '日本語国名': 'グレートブリテン及び北アイルランド連合王国',
#  '時間帯': '±0',
#  '最大都市': 'ロンドン',
#  '標語': '{{lang|fr|[[Dieu et mon droit]]}}<br />（[[フランス語]]:[[Dieu et mon '
#        'droit|神と我が権利]]）',
#  '水面積率': '1.3%',
#  '略名': 'イギリス',
#  '確立年月日1': '927年／843年',
#  '確立年月日2': '1707年{{0}}5月{{0}}1日',
#  '確立年月日3': '1801年{{0}}1月{{0}}1日',
#  '確立年月日4': '1927年{{0}}4月12日',
#  '確立形態1': '[[イングランド王国]]／[[スコットランド王国]]<br />（両国とも[[合同法 (1707年)|1707年合同法]]まで）',
#  '確立形態2': '[[グレートブリテン王国]]成立<br />（1707年合同法）',
#  '確立形態3': '[[グレートブリテン及びアイルランド連合王国]]成立<br />（[[合同法 (1800年)|1800年合同法]]）',
#  '確立形態4': '現在の国号「グレートブリテン及び北アイルランド連合王国」に変更',
#  '通貨': '[[スターリング・ポンド|UKポンド]] (£)',
#  '通貨コード': 'GBP',
#  '面積値': '244,820',
#  '面積大きさ': '1 E11',
#  '面積順位': '76',
#  '首相等氏名': '[[ボリス・ジョンソン]]',
#  '首相等肩書': '[[イギリスの首相|首相]]',
#  '首都': '[[ロンドン]]（事実上）'}
