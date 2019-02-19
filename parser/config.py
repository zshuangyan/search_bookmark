import os

INDEXER_FILE = "indexer.json"
DOC_WORD_FILE = "doc_word.json"
STOP_WORDS_FILE = "stopwords.txt"
DIR_PATH = os.path.dirname(__file__)

JIEBA_CHINESE_POS = ["n", "v", "vn"]
LINE_OF_PARAGRAPH = 20
MAX_WORDS = 1000