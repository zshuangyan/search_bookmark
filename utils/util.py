import random
import string
from datetime import datetime
import logging


def random_name():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))


def sequential_name(prefix="", base=0):
    def inner():
        nonlocal base
        result = "%s%s" % (prefix, base)
        base = base + 1
        return result

    return inner


class TimeUnitException(Exception):
    pass


def time_cost(time_unit="seconds"):
    unit_name = {"microseconds": "微秒",
                 "seconds": "秒",
                 "minutes": "分钟",
                 "hours": "小时"}
    if time_unit not in unit_name:
        raise TimeUnitException("时间单位只能是: microseconds(微秒) seconds(毫秒) hours(时), minutes(分), seconds(秒)")

    def decorator(func):
        def inner(*args, **kwargs):
            start = datetime.now()
            func(*args, **kwargs)
            end = datetime.now()
            duration = end - start
            value = getattr(duration, time_unit)
            logging.info("花费时间: %s%s" % (value, unit_name.get(time_unit)))

        return inner

    return decorator


get_name = sequential_name("默认名称")
