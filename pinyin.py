from pypinyin import lazy_pinyin, Style, pinyin

def hanzi_to_pinyin(text):
    # 带声调拼音
    pinyin_list = pinyin(text, style=Style.TONE)
    return pinyin_list
