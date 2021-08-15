# 28. MediaWikiマークアップの除去
# 27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，国の基本情報を整形せよ．

# 解法参考（25.）：
# https://qiita.com/FukuharaYohei/items/a0ae7f6548db309b7500

import gzip
import json

import re
# from collections import OrderedDict

# デバッグ用
from pprint import *

def load_json_gz(input_file):
    """
    20.py のJSONファイル読み込みを関数化
    """
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

def extract_body(data_str):
    r"""
    正規表現で文字列を抜き出す：ボディ部分

    {{基礎情報 ...
    }}

    の ... 部分を抜き出す

    >>> extract_body('''{{基礎情報 \nfoo\n}}''')
    'foo'
    """

    # 正規表現パターン
    pattern_body = r'''
        ^\{\{       # 最初の {{
        基礎情報.*?\n # 「基礎情報 国」+改行 ※非貪欲マッチ
        (.*?)       # 任意の文字列（0字以上）※キャプチャ（1番目）
        \n\}\}      # 終端の改行と「}}」
        $           # 文字列の末尾
    '''

    # 正規表現パターンを実行
    # 複数行にマッチさせる（フラグを「re.MULTILINE | re.DOTALL」にセット）
    # パターン文字列内で改行・コメントを入れる（フラグを「re.VERBOSE」にセット）
    re_body = re.search(pattern_body, data_str, re.MULTILINE | re.VERBOSE | re.DOTALL)
    str_body = re_body.group(1)

    return str_body

def extract_key_value(str_body):
    r"""
    正規表現で抜き出したものをリストに格納：キーと値

    >>> extract_key_value("|最大首都 = ロンドン\n")
    [('最大首都', 'ロンドン')]
    """
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

def replace_emph(str_input):
    """
    強調マークアップを除去

    >>> replace_emph("hoge")
    'hoge'
    >>> replace_emph("'foo'")
    "'foo'"
    >>> replace_emph("''bar''")
    'bar'
    >>> replace_emph("'''baz'''")
    'baz'
    """
    
    pattern = r"""
        [']{2,4}    # 「''」「'''」「''''」にマッチ
        (.+?)       # 任意の文字列（1文字以上）にマッチ ※非貪欲
        [']{2,4}    # 「''」「'''」「''''」にマッチ
    """
    str_replaced = re.sub(pattern, r"\1", str_input, flags=re.VERBOSE)
    return str_replaced

def replace_tag_pair(str_input):
    """
    HTMLタグを除去1: <foo attr="bar">...</foo> のパターン
    改行にマッチさせるため re.DOTALL を指定する

    >>> replace_tag_pair('<ref name="imf-statistics-gdp">[http://www.imf.org/external/pubs/ft/weo/2012/02/weodata/weorept.aspx?pr.x=70&pr.y=13&sy=2010&ey=2012&scsm=1&ssd=1&sort=country&ds=.&br=1&c=112&s=NGDP%2CNGDPD%2CPPPGDP%2CPPPPC&grp=0&a=IMF>Data and Statistics>World Economic Outlook Databases>By Countrise>United Kingdom]</ref>')
    ''
    """

    pattern = r"""
        <(.+?)>
        (.+?)
        </(.+?)>
    """
    str_replaced = re.sub(pattern, "", str_input, flags=re.VERBOSE | re.DOTALL)
    return str_replaced

def replace_tag_single(str_input):
    """
    HTMLタグを除去2: <foo /> のパターン
    改行にマッチさせるため re.DOTALL を指定する

    >>> replace_tag_single('<br />')
    ''
    """

    pattern = r"""
        <(.+?) />
    """
    str_replaced = re.sub(pattern, "", str_input, flags=re.VERBOSE | re.DOTALL)
    return str_replaced

def replace_template(str_input):
    """
    テンプレートを除去
    {{lang|en|foo}}

    >>> replace_template('{{lang|en|United Kingdom of Great Britain and Northern Ireland}}')
    'United Kingdom of Great Britain and Northern Ireland'
    """

    pattern = r"""
        \{\{
        .+?[|]
        .+[|]
        (.+?)
        \}\}
    """
    str_replaced = re.sub(pattern, r"\1", str_input, flags=re.VERBOSE)
    return str_replaced

def replace_inner_link(str_input):
    """
    内部リンクマークアップを除去
    [[文字列|hoge]]

    >>> replace_inner_link("[[:en:Brenda Hale, Baroness Hale of Richmond|ブレンダ・ヘイル]]")
    'Brenda Hale, Baroness Hale of Richmond'

    >>> replace_inner_link("[[ファイル:Royal Coat of Arms of the United Kingdom.svg|85px|イギリスの国章]]")
    'Royal Coat of Arms of the United Kingdom.svg'

    >>> replace_inner_link('[[イギリスの国章|国章]]')
    'イギリスの国章'

    >>> replace_inner_link('[[英語]]')
    '英語'
    """

    pattern = r"""
        \[\[                # 「[[」にマッチ
        (.+[:])?            # 任意の文字の後に「:」 ※例：[[:en:Brenda Hale, Baroness Hale of Richmond|ブレンダ・ヘイル]]
        ([^|]+?)            # 「|」以外の任意の文字列（1文字以上）にマッチ（非貪欲）
        (\|.+)*             # その後ろの「|hoge」（あとで削除する）
        \]\]                # 「]]」にマッチ
    """
    str_replaced = re.sub(pattern, r"\2", str_input, flags=re.VERBOSE)
    return str_replaced

def replace_outer_link(str_input):
    """
    外部リンクを除去
    [http(s)://...] , [http(s)://... タイトル]

    >>> replace_outer_link("[http://example.com]")
    ''

    >>> replace_outer_link("[https://example.com]")
    ''

    >>> replace_outer_link("[http://example.com/foo/bar.baz]")
    ''

    >>> replace_outer_link("[http://www.imf.org/external/pubs/ft/weo/2012/02/weodata/weorept.aspx?pr.x=70&pr.y=13&sy=2010&ey=2012&scsm=1&ssd=1&sort=country&ds=.&br=1&c=112&s=NGDP%2CNGDPD%2CPPPGDP%2CPPPPC&grp=0&a=IMF>Data and Statistics>World Economic Outlook Databases>By Countrise>United Kingdom]")
    'and Statistics>World Economic Outlook Databases>By Countrise>United Kingdom'

    >>> replace_outer_link("[http://warp.da.ndl.go.jp/info:ndljp/pid/1368617/www.meti.go.jp/policy/anpo/moto/topics/country/country.pdf 輸出貿易管理令等における国名表記の変更について]")
    '輸出貿易管理令等における国名表記の変更について'
    """

    pattern = r"""
        \[          # 「[」にマッチ
        (           # グループ開始
        https?      # http or https
        \://        # ://
        ([^\s]+)    # 非空白文字1字以上
        ?)          # グループ終了（非貪欲）
        (
        \s+(.+)     # 
        )?          # グループ終了（0回または1回出現）
        \]          # 「]」にマッチ
    """
    str_replaced = re.sub(pattern, r"\4", str_input, flags=re.VERBOSE)
    return str_replaced

def replace_zero_padding(str_input):
    """
    数値の0埋めを除去する: {{0}}

    >>> replace_zero_padding('1707年{{0}}5月{{0}}1日')
    '1707年5月1日'
    """

    pattern = r"""
        \{\{[0]\}\}
    """
    str_replaced = re.sub(pattern, "", str_input, flags=re.VERBOSE | re.DOTALL)
    return str_replaced

# ファイルの読み込み
input_file = "./jawiki-country.json.gz"
data = load_json_gz(input_file)

# データを絞る
data_str = data["text"]

# 正規表現で文字列を抜き出す：ボディ部分
str_body = extract_body(data_str)

# 正規表現で抜き出したものをリストに格納：キーと値
list_found = extract_key_value(str_body)

# 辞書に変換
dict_result = dict(list_found)

# 辞書の値を変換
dict_replaced = {}
for k, v in dict_result.items():
    # 強調マークアップを除去
    str_replaced = replace_emph(v)

    # HTMLタグを除去
    # 改行にマッチさせるため re.DOTALL を指定する
    # <foo attr="bar">...</foo> のパターン
    str_replaced = replace_tag_pair(str_replaced)
    # <foo /> のパターン
    str_replaced = replace_tag_single(str_replaced)

    # テンプレートを除去
    # {{lang|en|foo}} , {{lang:en:foo}}
    str_replaced = replace_template(str_replaced)

    # 内部リンクマークアップを除去
    # [[文字列|hoge]]
    str_replaced = replace_inner_link(str_replaced)

    # 外部リンクを除去
    # [http(s)://...] , [http(s)://... タイトル]
    str_replaced = replace_outer_link(str_replaced)

    # 数値の0埋めを除去する: {{0}}
    str_replaced = replace_zero_padding(str_replaced)

    # 置換した値を辞書に格納
    dict_replaced[k] = str_replaced

pprint(dict_replaced)

# テスト (doctest)
# python3 -m doctest -v 28.py
# （中略）
# 9 items passed all tests:
#    1 tests in 28.extract_body
#    1 tests in 28.extract_key_value
#    4 tests in 28.replace_emph
#    4 tests in 28.replace_inner_link
#    5 tests in 28.replace_outer_link
#    1 tests in 28.replace_tag_pair
#    1 tests in 28.replace_tag_single
#    1 tests in 28.replace_template
#    1 tests in 28.replace_zero_padding
# 19 tests in 11 items.
# 19 passed and 0 failed.
# Test passed.

# 結果
# {'GDP/人': '36,727',
#  'GDP値': '2兆3162億',
#  'GDP値MER': '2兆4337億',
#  'GDP値元': '1兆5478億',
#  'GDP統計年': '2012',
#  'GDP統計年MER': '2012',
#  'GDP統計年元': '2012',
#  'GDP順位': '6',
#  'GDP順位MER': '6',
#  'ISO 3166-1': 'GB / GBR',
#  'ccTLD': '.uk / .gb',
#  '人口値': '6643万5600',
#  '人口大きさ': '1 E7',
#  '人口密度値': '271',
#  '人口統計年': '2018',
#  '人口順位': '22',
#  '他元首等氏名1': 'Norman Fowler, Baron Fowler',
#  '他元首等氏名2': 'Lindsay Hoyle',
#  '他元首等氏名3': 'Brenda Hale, Baroness Hale of Richmond',
#  '他元首等肩書1': '貴族院 (イギリス)',
#  '他元首等肩書2': '庶民院 (イギリス)',
#  '他元首等肩書3': '連合王国最高裁判所',
#  '位置画像': 'United Kingdom (+overseas territories) in the World (+Antarctica '
#          'claims).svg',
#  '元首等氏名': 'エリザベス2世',
#  '元首等肩書': 'イギリスの君主',
#  '公式国名': 'United Kingdom of Great Britain and Northern Ireland',
#  '公用語': '英語',
#  '国旗画像': 'Flag of the United Kingdom.svg',
#  '国歌': 'United States Navy Band - God Save the Queen.ogg',
#  '国章リンク': '（イギリスの国章）',
#  '国章画像': 'Royal Coat of Arms of the United Kingdom.svg',
#  '国際電話番号': '44',
#  '地図画像': 'Europe-UK.svg',
#  '夏時間': '+1',
#  '建国形態': '建国',
#  '日本語国名': 'グレートブリテン及び北アイルランド連合王国',
#  '時間帯': '±0',
#  '最大都市': 'ロンドン',
#  '標語': '[[Dieu et mon droit）',
#  '水面積率': '1.3%',
#  '略名': 'イギリス',
#  '確立年月日1': '927年／843年',
#  '確立年月日2': '1707年5月1日',
#  '確立年月日3': '1801年1月1日',
#  '確立年月日4': '1927年4月12日',
#  '確立形態1': 'イングランド王国／スコットランド王国（両国とも合同法 (1707年)まで）',
#  '確立形態2': 'グレートブリテン王国成立（1707年合同法）',
#  '確立形態3': 'グレートブリテン及びアイルランド連合王国成立（合同法 (1800年)）',
#  '確立形態4': '現在の国号「グレートブリテン及び北アイルランド連合王国」に変更',
#  '通貨': 'スターリング・ポンド (£)',
#  '通貨コード': 'GBP',
#  '面積値': '244,820',
#  '面積大きさ': '1 E11',
#  '面積順位': '76',
#  '首相等氏名': 'ボリス・ジョンソン',
#  '首相等肩書': 'イギリスの首相',
#  '首都': 'ロンドン（事実上）'}
