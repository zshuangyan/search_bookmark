import math
import argparse
import logging
import logging.config

from parser.indexer import get_indexer
from .models import SearchResult
from utils.db import query as query_doc
from log_config import LOGGING

logging.config.dictConfig(LOGGING)

indexer = get_indexer()
doc_num, index = indexer["doc_num"], indexer["index"]


def get_args():
    search_arg = argparse.ArgumentParser()
    search_arg.add_argument("query", help="search content")
    search_arg.add_argument("-n", "--num", type=int, default=10, help="num of docs returned")
    return vars(search_arg.parse_args())


def search(query, **kwargs):
    # Todo: 如果是中文, 要先进行分词, 不能直接split
    words = query.split()
    doc_set = set()
    # Todo: 如果支持模糊查找, 同义词查找, 是把符合要求的词的倒排索引和并起来处理么?
    for word in words:
        doc_list = index.get(word)
        if doc_list:
            doc_set |= set(doc_id for doc_id, _ in doc_list)

    doc_word_tf_idf = {doc_id: {word: 0 for word in words} for doc_id in doc_set}
    for word in words:
        doc_list = index.get(word)
        if doc_list:
            num = len(doc_list)
            df = math.log10(doc_num / num)
            for doc_id, word_frequency in doc_list:
                doc_word_tf_idf[doc_id][word] = df * word_frequency

    doc_score = {key: sum(value.values()) for key, value in doc_word_tf_idf.items()}
    docs = sorted(doc_score.items(), reverse=True, key=lambda x: x[1])
    if "num_limit" in kwargs:
        docs = docs[:kwargs.get("num_limit")]
    # Todo: 目前只显示了文档id和评分, 最重要的是要把文档内容也展示出来
    results = []
    for doc_id, score in docs:
        doc_data_set = query_doc("select * from entry where id = %s" % doc_id)
        url = doc_data_set["url"][0]
        content = doc_data_set["doc"][0][:100]
        results.append({"id": doc_id, "url": url, "content": content, "score": score})

    return SearchResult(found=True, results=results)


if __name__ == "__main__":
    args = get_args()
    logging.info("输入参数解析结果: %s" % args)
    result = search(args["query"], num_limit=args["num"])
    print(result)
