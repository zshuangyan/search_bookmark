import unittest
from ..models import Word


class TestMatchWord(unittest.TestCase):
    def test_word_match_when_length_equal(self):
        word = Word("precize", fuzzy=1, weights=1)
        self.assertTrue(word.match("precise"))

    def test_word_match_when_length_diff(self):
        word = Word("completed", fuzzy=1, weights=1)
        self.assertTrue(word.match("complete"))

    def test_word_not_match_when_length_equal(self):
        word = Word("angle", fuzzy=1, weights=1)
        self.assertFalse(word.match("angel"))

    def test_word_not_match_when_length_not_equal(self):
        word = Word("handsome", fuzzy=2, weights=1)
        self.assertFalse(word.match("hand"))

        word = Word("wall", fuzzy=2, weights=1)
        self.assertFalse(word.match("wollet"))

        word = Word("watch", fuzzy=2, weights=1)
        self.assertFalse(word.match("what"))