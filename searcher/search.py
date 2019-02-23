import math

from parser.indexer import get_indexer
from .models import SearchResult, Word

indexer = get_indexer()
doc_num, index = indexer["doc_num"], indexer["index"]


def search(query, **kwargs):
    words = query.split()
    doc_set = set()
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
    results = sorted(doc_score.items(), reverse=True, key=lambda x: x[1])
    if "num_limit" in kwargs:
        results = results[:kwargs.get("num_limit")]
    return SearchResult(found=True, results=results)


if __name__ == "__main__":
    print(search("java"))
