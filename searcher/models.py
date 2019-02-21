class SearchResult:
    def __init__(self, found, results):
        self.found = found
        self.results = results

    def __str__(self):
        return "Found: %s, Results: \n%s" % (self.found, self.results)


class SearchCondition:
    def __init__(self, query):
        pass

class FilterCondition:
    def __init__(self):
        pass