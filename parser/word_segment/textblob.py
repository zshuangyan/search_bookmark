from textblob import TextBlob, Word
import logging

ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'


def textblob_word_segment(text):
    blob = TextBlob(text)
    return blob.pos_tags


def normalize(word, pos):
    w = Word(word)
    try:
        if pos.startswith("N"):
            result = w.singularize()
        else:
            tag = _penn_to_wordnet(pos)
            if tag:
                result = w.lemmatize(tag)
                logging.debug("单词: (%s, %s), 归一化后: %s" % (word, pos, result))
            else:
                result = word
    except Exception as e:
        logging.error("单词: (%s, %s), 归一化出错: %s" % (word, pos, e))
        result = word
    return result


def _penn_to_wordnet(tag):
    """Converts a Penn corpus tag into a Wordnet tag."""
    if tag.startswith("N"):
        return NOUN
    if tag.startswith("J"):
        return ADJ
    if tag.startswith("V"):
        return VERB
    if tag.startswith("R"):
        return ADV
    return None
