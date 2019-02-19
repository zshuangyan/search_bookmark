import random
import string


def random_name():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))


def sequential_name(prefix="", base=0):
    def inner():
        nonlocal base
        result = "%s%s" % (prefix, base)
        base = base + 1
        return result
    return inner


get_name = sequential_name("默认名称")
