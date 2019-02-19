from lxml import etree, html
import os

DIR_PATH = os.path.dirname(__file__)

with open(os.path.join(DIR_PATH, "test.html")) as f:
    text = f.read()
    doc = etree.HTML(text)
    result = doc.xpath('/html/body/dl/dt')[0]
    print("使用etree.HMTL接口")
    print("能够正确解析子元素个数: ", len(result) == 2)

    print("---------------------------------------------")

    doc1 = html.fromstring(text)
    result = doc1.xpath('/html/body/dl/dt')[0]
    print("使用html.fromstring接口")
    print("能够正确解析子元素个数: ", len(result) == 2)

print("---------------------------------------------")

html1 = etree.parse(os.path.join(DIR_PATH, "test.html"))
result = html1.xpath('/html/body/dl/dt')[0]
print("使用etree.parse接口")
print("能够正确解析子元素个数: ", len(result) == 2)

print("---------------------------------------------")

html2 = html.parse(os.path.join(DIR_PATH, "test.html"))
result = html2.xpath("/html/body/dl/dt")[0]
print("使用html.parse接口")
print("能够正确解析子元素个数: ", len(result) == 2)

