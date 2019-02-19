from lxml import html
import re


def clean(text):
    # 除去多余的空格
    text = re.sub(r"[ \t\r\f\v]+", " ", text)

    # 除去多余的空行
    text = re.sub(r"\n+", "\n", text)

    # 除去占用超过3个字节的字符, 否则MySQL会报错
    text = ''.join(c for c in text if c < '\U00010000')

    # 如果只有空白字符, 那么返回空字符
    return text.strip()


def extract_text(content: str):
    """
    Extract only text data from html pages.

    Args:
        content: html page in string format

    Returns:
        text
    """
    doc = html.document_fromstring(content, parser=html.HTMLParser(remove_comments=True))
    body = doc.find("body")
    texts = []
    for element in body.iter():
        # 标签的文本部分不为空
        if element.text:
            # 处理文本
            text = clean(element.text)
            if text:
                texts.append(text)

    return "\n".join(texts)
