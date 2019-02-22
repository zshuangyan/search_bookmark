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