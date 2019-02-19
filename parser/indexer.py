from records import Record
from datetime import datetime
from sys import getsizeof
import os
import json
import operator

from utils.db import query
from .config import DIR_PATH, INDEXER_FILE, DOC_WORD_FILE
from .word_frequency import get_word_frequency_from_api


def process_docs(docs_dataset):
    invert_index = {}
    doc_word_frequency = {}
    for row in docs_dataset:
        record = Record(keys=docs_dataset.headers, values=row)
        word_frequency = get_word_frequency_from_api(record.doc)
        doc_word_frequency[record.id] = word_frequency
        for word, frequency in word_frequency.items():
            if word in invert_index:
                invert_index[word].append((record.id, frequency))
            else:
                invert_index[word] = [(record.id, frequency)]
    return invert_index, doc_word_frequency


def create_index():
    start = datetime.now()
    docs = query("select * from entry")
    end = datetime.now()
    print("加载数据耗时: %ss" % (end - start).seconds)

    start = datetime.now()
    index, doc_word = process_docs(docs)
    end = datetime.now()
    print("创建索引耗时: %ss" % (end - start).seconds)
    print("文档总数: %s" % len(doc_word))
    print("单词总数: %s" % len(index))
    print("单词文档倒排表大小: %s" % getsizeof(index))
    print("文档单词字典大小: %s" % getsizeof(doc_word))

    sorted_index = sorted(index, key=operator.itemgetter(1))
    for item in sorted_index[:200]:
        print(item)
    print("过滤掉文档频率集较高的词汇")
    doc_num = len(doc_word)
    index = {word: doc_list for word, doc_list in index.items() if doc_num / len(doc_list) > 3}
    print("单词总数: %s" % len(index))
    print("单词文档倒排表大小: %s" % getsizeof(index))

    with open(os.path.join(DIR_PATH, INDEXER_FILE), "w") as f:
        json.dump(index, f)

    with open(os.path.join(DIR_PATH, DOC_WORD_FILE), "w") as f:
        json.dump(doc_word, f)


def get_index():
    with open(os.path.join(DIR_PATH, INDEXER_FILE), "w") as f:
        index = json.load(f)

    with open(os.path.join(DIR_PATH, DOC_WORD_FILE), "w") as f:
        doc_word = json.load(f)

    return index, doc_word


if __name__ == "__main__":
    create_index()
