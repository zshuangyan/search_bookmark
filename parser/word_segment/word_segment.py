import logging
from parser.config import MAX_WORDS
from parser.util import group
from .stanford_word_segment import stanford_word_segment
from .jieba_word_segment import jieba_word_segment, get_doc_lang
from .textblob import textblob_word_segment


def word_segment(text):
    def inner(inner_text):
        if not inner_text.strip():
            return []
        try:
            lang = get_doc_lang(inner_text)
            logging.info("当前文档语言: %s" % lang)
        except Exception as e:
            logging.error("无法获取当前段落语言: %s, 段落内容:\n%s" % (e, inner_text))
            return []
        return _word_segment(inner_text, lang)

    lines = [line for line in text.split("\n") if line.strip()]
    logging.info("当前文档总行数: %s" % len(lines))
    if len(text) > MAX_WORDS:
        total_word_pos = []
        paragraphs = group(text, group_size=MAX_WORDS)
        for pg in paragraphs:
            word_pos = inner(pg)
            if not word_pos:
                logging.error("当前分词结果为空, 文档内容: %s, 文档所有段落: %s" % (pg, paragraphs))
                continue
            logging.debug("当前分词结果: %s" % word_pos)
            total_word_pos.extend(word_pos)
        result = total_word_pos
    else:
        result = inner(text)
    logging.info("文档分词结果: %s" % result)
    return result


def _word_segment(text, lang):
    if not text:
        raise Exception("文本不能为空")
    if lang == "en":
        return textblob_word_segment(text)
    elif lang == "zh_en":
        try:
            return stanford_word_segment(text, lang='zh')
        except Exception as e:
            logging.error("调用斯坦福分词API出错: %s, 分词内容: \n%s" % (e, text[:50]))
            return jieba_word_segment(text)
    else:
        return jieba_word_segment(text)
