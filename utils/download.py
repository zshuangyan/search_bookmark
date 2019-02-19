import requests

OK_CODE = [200]
REDIRECT_CODE = [301, 302]
REDIRECT_TIMES_LIMIT = 5


class RedirectExceed(Exception):
    pass


class RedirectUrlNotExist(Exception):
    pass


class ResponseError(Exception):
    pass


def download(url, redirect_times=0):
    """get content of url.

    Args:
        url
        redirect_times
        
    Raises:
        RedirectExceed if redirect times exceed limit times
        RedirectUrlNotExist if can not get location from header
        ResponseError if response code is 4xx or 5xx
        
    Returns:
        content
    """
    if redirect_times == REDIRECT_TIMES_LIMIT:
        raise RedirectExceed("重定向次数超过限制次数: %s" % REDIRECT_TIMES_LIMIT)
    res = requests.get(url, timeout=3)
    if res.status_code in REDIRECT_CODE:
        redirect_url = res.headers.get("Location", "")
        if redirect_url:
            return download(redirect_url, redirect_times + 1)
        else:
            raise RedirectUrlNotExist("重定向地址不存在")
    elif res.status_code in OK_CODE:
        return res.content
    else:
        raise ResponseError("响应错误")
