from records import Record
from datetime import datetime
from sys import getsizeof
import os
import json

from utils.db import query
from .config import DIR_PATH, INDEXER_FILE, DOC_WORD_FILE
from .word_segment import word_segment
from .util import clean_words, get_word_frequency


def process_docs(docs_dataset):
    invert_index = {}
    doc_word_frequency = {}
    for row in docs_dataset:
        record = Record(keys=docs_dataset.headers, values=row)
        # 分词并获取词性
        words_pos = word_segment(record.doc)
        # 清洗单词
        words = clean_words(words_pos)
        word_frequency = get_word_frequency(words)
        doc_word_frequency[record.id] = word_frequency
        for word, frequency in word_frequency.items():
            if word in invert_index:
                invert_index[word].append((record.id, frequency))
            else:
                invert_index[word] = [(record.id, frequency)]
    return invert_index, doc_word_frequency


def create_index():
    docs = query("select * from entry")

    start = datetime.now()
    index, doc_word = process_docs(docs)
    end = datetime.now()
    print("创建索引耗时: %ss" % (end - start).seconds)
    print("文档总数: %s" % len(doc_word))
    print("单词总数: %s" % len(index))
    print("单词文档倒排表大小: %s" % getsizeof(index))
    print("文档单词字典大小: %s" % getsizeof(doc_word))

    print("过滤掉文档频率集较高的词汇")
    doc_num = len(doc_word)
    index = {word: doc_list for word, doc_list in index.items() if doc_num / len(doc_list) > 3}
    print("单词总数: %s" % len(index))
    print("单词文档倒排表大小: %s" % getsizeof(index))

    with open(os.path.join(DIR_PATH, INDEXER_FILE), "w") as f:
        json.dump(index, f)

    with open(os.path.join(DIR_PATH, DOC_WORD_FILE), "w") as f:
        json.dump(doc_word, f)

    long_word_index = {word: doc_list for word, doc_list in index.items() if len(word) > 15}
    print("长单词倒排表大小: %s" % getsizeof(long_word_index))
    with open(os.path.join(DIR_PATH, "long_word_index.json"), "w") as f:
        json.dump(long_word_index, f)

    normal_word_index = {word: doc_list for word, doc_list in index.items() if len(word) > 1}
    print("普通单词倒排表大小: %s" % getsizeof(normal_word_index))
    with open(os.path.join(DIR_PATH, "normal_word_index.json"), "w") as f:
        json.dump(normal_word_index, f)


def get_index():
    with open(os.path.join(DIR_PATH, INDEXER_FILE), "w") as f:
        index = json.load(f)

    with open(os.path.join(DIR_PATH, DOC_WORD_FILE), "w") as f:
        doc_word = json.load(f)

    return index, doc_word


if __name__ == "__main__":
    create_index()
