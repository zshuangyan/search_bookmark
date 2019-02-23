class SearchResult:
    def __init__(self, found, results):
        self.found = found
        self.results = results

    def __str__(self):
        return "Found: %s, Results: \n%s" % (self.found, self.results)


class Word:
    def __init__(self, raw, weights, fuzzy):
        self.raw = raw
        self.weights = weights
        self.fuzzy = fuzzy

    def __str__(self):
        return "word content: %s, weights: %s, fuzzy: %s" % (self.raw, self.weights, self.fuzzy)

    def match(self, value: str):
        def compare(word1, word2, fuzzy):
            count = 0
            for i in range(len(word2)):
                if word1[i] != word2[i]:
                    count += 1
                    if count > fuzzy:
                        return False
            return True

        def loop_compare(large_word, small_word, fuzzy):
            times = len(large_word) - len(small_word)
            small_len = len(small_word)
            for i in range(times):
                if compare(large_word[i: i + small_len], small_word, fuzzy):
                    return True
            return False

        if not self.fuzzy:
            return value == self.raw
        if len(self.raw) == len(value):
            return compare(self.raw, value, self.fuzzy)

        # 长度差异和字符差异等同
        len_diff = abs(len(self.raw) - len(value))
        if len_diff > self.fuzzy:
            return False

        # 检查字符差异
        word_diff_limit = self.fuzzy - len_diff
        if len(self.raw) > len(value):
            return loop_compare(self.raw, value, word_diff_limit)
        else:
            return loop_compare(value, self.raw, word_diff_limit)
