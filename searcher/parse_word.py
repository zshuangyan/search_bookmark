import re
from .models import Word

MAX_LEN = 30
WORD_REGEXP = re.compile("[^~]{1,20}((?:~)[1-9]?)?((?:\^)[1-9]?)?")


class WordFormatError(Exception):
    pass


def parse_word(word):
    # 检查单词长度不超过指定格式
    if len(word) > MAX_LEN:
        raise WordFormatError("单词长度上限为: %s" % MAX_LEN)
    match = re.match(WORD_REGEXP, word)
    if not match:
        raise WordFormatError("单词格式错误, 请以类似wonder~2^3的形式")
    word = match.group()
    # 从后往前解析, 先解析权重
    weights_index = word.find("^")
    if weights_index == -1:
        weights = 1
    elif weights_index == len(word) - 1:
        word = word[:-1]
        weights = 1
    else:
        weights = int(word[weights_index + 1:])
        word = word[:weights_index]

    # 解析模糊量
    fuzzy_index = word.find("~")
    if fuzzy_index == -1:
        fuzzy = 0
        raw = word
    elif fuzzy_index == len(word) - 1:
        raw = word[:-1]
        fuzzy = min(len(raw) // 2, 2)
    else:
        raw = word[:fuzzy_index]
        fuzzy = min(len(word), int(word[fuzzy_index + 1:]))

    # 单词归一化为小写形式
    raw = raw.lower()

    return Word(raw, fuzzy=fuzzy, weights=weights)
