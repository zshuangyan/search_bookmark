from collections import Counter
import logging
import re

from .config import JIEBA_CHINESE_POS
from .word_segment.textblob import normalize

SEPS = ["-", "_", "\.", "\/"]


def get_stop_words(file_path):
    with open(file_path) as f:
        result = f.readlines()
        result = [r for r in result if r.strip()]
        return result


def group(elements, group_size):
    index = 0
    total_elements = len(elements)
    groups = []
    while index < total_elements:
        current_group = elements[index: index + group_size]
        if current_group.strip():
            groups.append(current_group)
        index += group_size
    return groups


def get_word_frequency(words):
    counter = Counter()
    for word in words:
        counter[word] += 1
    return counter


def filter_words_by_pos(pos):
    if pos in JIEBA_CHINESE_POS or pos.startswith("N") or pos.startswith("V") or pos.startswith("J"):
        return True
    else:
        return False


def filter_words_by_length(word_len):
    return 1 < word_len < 30


def english(word):
    return not any(map(lambda x: ord(x) >= 128, word))


def split_word(word):
    result = [word for word in re.split("|".join(SEPS), word) if len(word) > 1]
    logging.debug("分解单词: %s" % result)
    return result


def clean_words(words_pos):
    if not words_pos:
        return []
    total_words = len(words_pos)
    logging.info("清洗前单词总量: %s" % total_words)

    # 通过词性过滤单词
    words_pos = [(word, pos) for word, pos in words_pos if filter_words_by_pos(pos)]

    # 归一化, 不需要处理中文
    normal_words = [normalize(word, pos) if english(word) else word for word, pos in words_pos]

    # 如果单词长度较长, 处理中间含有连接符的情况
    words_nested = [split_word(word) for word in normal_words]
    words = [word for nest in words_nested for word in nest]

    # 过滤掉过长或者过短的单词, 并把单词转换为小写形式
    words = [word.lower() for word in words if filter_words_by_length(len(word))]

    logging.info("清洗后单词总量: %s" % len(words))
    return words


def remove_consecutive_words(words):
    before = ""
    index_to_remove = []
    for index, word in enumerate(words):
        if word == before:
            index_to_remove.append(index)
        else:
            before = word
    return [word for index, word in enumerate(words) if index not in index_to_remove]
