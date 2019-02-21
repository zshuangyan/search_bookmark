from records import Record
from datetime import datetime
from sys import getsizeof
import os
import json
import logging
from logging.config import dictConfig

from utils.db import query
from .config import DIR_PATH, INDEXER_FILE
from .word_segment import word_segment
from .util import clean_words, get_word_frequency


def process_docs(docs_dataset):
    invert_index = {}
    for row in docs_dataset:
        record = Record(keys=docs_dataset.headers, values=row)
        logging.info("处理文档: %s" % record.id)
        if not record.doc.strip():
            logging.warning("文档内容为空")
            continue
        # 分词并获取词性
        words_pos = word_segment(record.doc)
        # 清洗单词
        words = clean_words(words_pos)
        word_frequency = get_word_frequency(words)
        for word, frequency in word_frequency.items():
            if word in invert_index:
                invert_index[word].append((record.id, frequency))
            else:
                invert_index[word] = [(record.id, frequency)]
    return invert_index


def create_indexer():
    docs = query("select * from entry")

    start = datetime.now()
    index = process_docs(docs)
    end = datetime.now()
    logging.debug("创建索引耗时: %ss" % (end - start).seconds)
    logging.info("文档总数: %s" % len(docs))
    logging.info("单词总数: %s" % len(index))
    logging.info("单词倒排表大小: %s" % getsizeof(index))

    logging.info("基于df过滤词汇, df的值需大于3")
    doc_num = len(docs)
    index = {word: doc_list for word, doc_list in index.items() if doc_num / len(doc_list) > 3}
    logging.info("单词总数: %s" % len(index))
    logging.info("单词文档倒排表大小: %s" % getsizeof(index))

    indexer = {"doc_num": doc_num, "index": index}

    with open(os.path.join(DIR_PATH, INDEXER_FILE), "w") as f:
        json.dump(indexer, f)


def get_indexer():
    with open(os.path.join(DIR_PATH, INDEXER_FILE), "r") as f:
        indexer = json.load(f)
    return indexer


if __name__ == "__main__":
    from log_config import LOGGING
    dictConfig(LOGGING)
    create_indexer()
