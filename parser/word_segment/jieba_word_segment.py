import jieba.posseg as pseg
import os
import logging

from parser.util import get_stop_words
from parser.config import DIR_PATH, STOP_WORDS_FILE, JIEBA_CHINESE_POS
from .textblob import textblob_word_segment


def jieba_word_segment(text):
    stop_words = get_stop_words(os.path.join(DIR_PATH, STOP_WORDS_FILE))
    words = pseg.cut(text)
    words = list(words)
    eng_words = [word for word, flag in words if flag == "eng"]
    if eng_words:
        try:
            eng_words_pos = process_eng(eng_words)
        except Exception as e:
            logging.error("调用textblob分词出错: %s" % e)
            eng_words_pos = [(word, "eng") for word in eng_words]
    else:
        eng_words_pos = []

    chinese_words_pos = [(word, flag) for word, flag in words if
                         flag in JIEBA_CHINESE_POS and len(word) > 1 and word not in stop_words]
    return eng_words_pos + chinese_words_pos


def process_eng(eng_words):
    return textblob_word_segment(" ".join(eng_words))


def get_doc_lang(text):
    words = pseg.cut(text)
    words = {word: flag for word, flag in words}
    chinese_words = [word for word, flag in words.items() if flag not in ["eng", "x", "m"]]
    eng_words = [word for word, flag in words.items() if flag == "eng"]

    if (not chinese_words) and (not eng_words):
        raise Exception("无法从文本中过滤出中文和英文, 结巴分词结果: %s" % words)
    chinese_words_ratio = len(chinese_words) / (len(chinese_words) + len(eng_words))
    logging.info("中文单词占比: %s" % chinese_words_ratio)
    if chinese_words_ratio < 0.3:
        return "en"
    elif chinese_words_ratio > 0.6:
        return "zh"
    else:
        return "zh_en"
