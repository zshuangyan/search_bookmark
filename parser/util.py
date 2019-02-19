import jieba.posseg as pseg
from collections import Counter

from .config import JIEBA_CHINESE_POS


def group(elements, group_size, sep):
    index = 0
    total_elements = len(elements)
    groups = []
    while index < total_elements:
        groups.append(sep.join(elements[index: group_size]))
        index += group_size
    return groups


def get_word_frequency(words):
    counter = Counter()
    for word in words:
        counter[word] += 1
    return counter


def filter_words_by_pos(pos):
    if pos in JIEBA_CHINESE_POS or pos.startswith("N") or pos.startswith("V"):
        return True
    else:
        return False


def filter_words_by_length(word_len):
    return 1 < word_len < 30


def clean_words(words_pos):
    if not words_pos:
        return []
    total_words = len(words_pos)
    print("单词总量: %s" % total_words)

    normal_words = [word for word, pos in words_pos if filter_words_by_pos(pos)]

    # 过滤掉过长或者过短的单词
    normal_words = [word for word in normal_words if filter_words_by_length(len(word))]

    # Todo: 处理中间含有连接符的单词
    normal_num = len(normal_words)
    print("过滤后单词总量: %s" % normal_num)
    print("清洗无关单词比例: %s" % (1 - normal_num / total_words))

    # Todo: 单词形式归一化
    # 单词转化为小写形式
    return [word.lower() for word in normal_words]


def get_doc_lang(text):
    words = pseg.cut(text)
    words = {word: flag for word, flag in words}
    chinese_words = [word for word, flag in words.items() if flag in JIEBA_CHINESE_POS]
    eng_words = [word for word, flag in words.items() if flag == "eng"]

    if not chinese_words and eng_words:
        raise Exception("text is empty")
    chinese_words_ratio = len(chinese_words) / len(chinese_words) + len(eng_words)
    if chinese_words_ratio < 0.2:
        return "en"
    elif chinese_words_ratio > 0.8:
        return "zh"
    else:
        return "zh_en"


def remove_consecutive_words(words):
    before = ""
    index_to_remove = []
    for index, word in enumerate(words):
        if word == before:
            index_to_remove.append(index)
        else:
            before = word
    return [word for index, word in enumerate(words) if index not in index_to_remove]
