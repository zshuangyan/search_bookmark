import unittest
from ..parse_word import parse_word, WordFormatError, MAX_LEN


class WordParseTest(unittest.TestCase):
    def test_only_word_in_chinese(self):
        word = "中午"
        result = parse_word(word)
        assert result.raw == word
        assert result.weights == 1
        assert result.fuzzy == 0

    def test_only_word_in_english(self):
        word = "wonderful"
        result = parse_word(word)
        assert result.raw == word
        assert result.weights == 1
        assert result.fuzzy == 0

    def test_word_length_exceed(self):
        word = "h" * (MAX_LEN + 1)
        self.assertRaises(WordFormatError, parse_word, word)

    def test_word_with_fuzzy(self):
        word = "hadoop~1"
        result = parse_word(word)
        assert result.raw == "hadoop"
        assert result.weights == 1
        assert result.fuzzy == 1

        word = "hadoop~"
        result = parse_word(word)
        assert result.raw == "hadoop"
        assert result.weights == 1
        assert result.fuzzy == 2

    def test_word_with_weights(self):
        word = "人工智能^3"
        result = parse_word(word)
        assert result.raw == "人工智能"
        assert result.weights == 3
        assert result.fuzzy == 0

        word = "人工智能^"
        result = parse_word(word)
        assert result.raw == "人工智能"
        assert result.weights == 1
        assert result.fuzzy == 0

    def test_word_with_fuzzy_and_weight(self):
        word = "hadoop~1^3"
        result = parse_word(word)
        assert result.raw == "hadoop"
        assert result.weights == 3
        assert result.fuzzy == 1

        word = "hadoop~^3"
        result = parse_word(word)
        assert result.raw == "hadoop"
        assert result.weights == 3
        assert result.fuzzy == 2

        word = "hadoop~1^"
        result = parse_word(word)
        assert result.raw == "hadoop"
        assert result.weights == 1
        assert result.fuzzy == 1

        word = "hadoop~^"
        result = parse_word(word)
        assert result.raw == "hadoop"
        assert result.weights == 1
        assert result.fuzzy == 2