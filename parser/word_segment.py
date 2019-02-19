import jieba.posseg as pseg
from datetime import datetime
import time
import requests
import os
from .config import DIR_PATH, STOP_WORDS_FILE, JIEBA_CHINESE_POS, MAX_WORDS, LINE_OF_PARAGRAPH
from .util import remove_consecutive_words, group, get_doc_lang


def get_stop_words(file_path):
    with open(file_path) as f:
        result = f.readlines()
        result = [r for r in result if r.strip()]
        return result


def word_segment(text):
    lines = text.split("\n")
    if len(lines) > LINE_OF_PARAGRAPH:
        total_word_pos = []
        paragraphs = group(lines, group_size=LINE_OF_PARAGRAPH, sep="\n")
        for pg in paragraphs:
            if not pg.strip():
                continue
            try:
                lang = get_doc_lang(pg)
                print("当前段落语言: %s" % lang)
            except Exception as e:
                print("无法获取当前段落语言: %s, 段落内容: %s" % (e, pg))
                continue
            word_pos = _word_segment(pg, lang)
            print("分词结果: %s" % word_pos)
            total_word_pos.extend(word_pos)
            return total_word_pos
    else:
        if not text.strip():
            return []
        try:
            lang = get_doc_lang(text)
        except Exception as e:
            print("无法获取当前文档语言: %s, 文档内容: %s" % (e, text))
            return []
        return _word_segment(text, lang)


def word_segment_from_api(text, lang="en"):
    url = "http://corenlp.run/"
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    properties = '{"annotators":"tokenize,ssplit,pos", "date": "%s", "outputFormat":"json"}' % date
    params = {"properties": properties, "pipelineLanguage": lang}
    result = requests.post(url, data=text.encode("utf-8"), params=params)
    if result.status_code != 200:
        print("错误码: %s, 响应内容: %s" % (result.status_code, result.content))
        raise Exception(result.content)
    sentences = result.json()["sentences"]
    tokens = [token for sentence in sentences for token in sentence["tokens"]]
    words_pos = [(token["word"], token["pos"]) for token in tokens]
    time.sleep(0.3)
    return words_pos


def word_segment_from_jieba(text):
    stop_words = get_stop_words(os.path.join(DIR_PATH, STOP_WORDS_FILE))
    words = pseg.cut(text)
    words = list(words)
    eng_words = [word for word, flag in words if flag == "eng"]
    if eng_words:
        eng_words_pos = process_eng_in_jieba(eng_words)
    else:
        eng_words_pos = []

    chinese_words_pos = [(word, flag) for word, flag in words if
                         flag in JIEBA_CHINESE_POS and len(word) > 1 and word not in stop_words]
    return eng_words_pos + chinese_words_pos


def process_eng_in_jieba(eng_words):
    print("结巴处理得到的英文单词总数: %s" % len(eng_words))
    eng_words = remove_consecutive_words(eng_words)
    print("清理重复的单词后单词数", len(eng_words))
    if len(eng_words) > MAX_WORDS:
        groups = group(eng_words, group_size=MAX_WORDS, sep=" ")
        total_words_pos = []
        for g in groups:
            group_words_pos = word_segment_from_api(g, "en")
            total_words_pos.extend(group_words_pos)
        return total_words_pos
    else:
        return word_segment_from_api(" ".join(eng_words), "en")


def _word_segment(text, lang):
    if not text:
        raise Exception("文本不能为空")
    if lang == "en":
        return word_segment_from_api(text, "en")
    elif lang == "zh_en":
        return word_segment_from_api(text, "zh")
    else:
        return word_segment_from_jieba(text)
