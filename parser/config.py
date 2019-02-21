import os

INDEXER_FILE = "indexer.json"
STOP_WORDS_FILE = "stopwords.txt"
DIR_PATH = os.path.dirname(__file__)

JIEBA_CHINESE_POS = ["n", "v", "vn"]
MAX_WORDS = 800