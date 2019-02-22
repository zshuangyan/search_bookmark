from datetime import datetime
import requests
import logging
import time


def stanford_word_segment(text, lang="en"):
    url = "http://corenlp.run/"
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    properties = '{"annotators":"tokenize,ssplit,pos", "date": "%s", "outputFormat":"json"}' % date
    params = {"properties": properties, "pipelineLanguage": lang}
    result = requests.post(url, data=text.encode("utf-8"), params=params)
    if result.status_code != 200:
        logging.debug("错误码: %s, 响应内容: %s" % (result.status_code, result.content))
        raise Exception(result.content)
    sentences = result.json()["sentences"]
    tokens = [token for sentence in sentences for token in sentence["tokens"]]
    words_pos = [(token["word"], token["pos"]) for token in tokens]
    time.sleep(0.3)
    return words_pos