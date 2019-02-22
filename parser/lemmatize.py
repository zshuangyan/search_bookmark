from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from datetime import datetime

lemma = WordNetLemmatizer()
stemmer = PorterStemmer()


def time_cost(time_unit="microseconds"):
    unit_name = {"microseconds": "微秒",
                 "seconds": "秒",
                 "minutes": "分钟",
                 "hours": "小时"}
    if time_unit not in unit_name:
        raise Exception("时间单位只能是: hours(时), minutes(分), seconds(秒)")

    def decorator(func):
        def inner(*args, **kwargs):
            start = datetime.now()
            func(*args, **kwargs)
            end = datetime.now()
            duration = end - start
            value = getattr(duration, time_unit)
            print("花费时间: %s%s" % (value, unit_name.get(time_unit)))

        return inner

    return decorator


@time_cost(time_unit="seconds")
def lm():
    print(lemma.lemmatize('previous'))
    print(lemma.lemmatize('helpful'))
    print(lemma.lemmatize('completed'))
    print(lemma.lemmatize('worked', pos='v'))
    print(lemma.lemmatize('Scheduled', pos='v'))
    print(lemma.lemmatize('bookmarked', pos='v'))


@time_cost()
def st():
    print(stemmer.stem('previous'))
    print(stemmer.stem('helpful'))
    print(stemmer.stem('completed'))
    print(stemmer.stem('worked'))
    print(stemmer.stem('Scheduled'))


lm()
st()
