# -*- coding: utf-8 -*-
"""解析Chrome收藏夹

Chrome收藏夹的嵌套结构和Linux系统的目录结果很类似, Linux系统的根目录是/,每个目录下可以包含子目录和文件.
Chrome的根目录名字是"工具栏", 工具栏中可以包含URL链接, 也可以包含新的目录
"""
from lxml import etree
from records import Record
from tablib import Dataset
import os
import concurrent.futures

from utils.util import get_name
from utils.download import download
from utils.db import save
from crawl.util import extract_text
from crawl.config import DIR_PATH, FILE_NAME, ROOT_XPATH, CONTENT_INDEX, CHILD_XPATH
from element import Element

# 解析文档
doc = etree.parse(os.path.join(DIR_PATH, FILE_NAME))
# 获取收藏夹的根节点
root = doc.xpath(ROOT_XPATH)[0]


def visit(elem, depth=0):
    content = elem[CONTENT_INDEX]
    # 解析名字
    name = content.text
    if name is None or name.strip() == "":
        name = get_name()

    # 如果是a标签, 则需提取url
    if content.tag == "a":
        urls = content.get("href"),
        url = urls[0]
        createds = content.get("add_date"),
        created = createds[0]
        record = Record(keys=["url", "created"], values=[url, created])
    else:
        record = None
    elem_obj = Element(name=name, data=record)
    for child in elem.findall(CHILD_XPATH):
        elem_obj.add_child(visit(child, depth + 1))
    return elem_obj


def download_and_save(leaves):
    dataset = Dataset()
    dataset.title = "entry"
    dataset.headers = ("name", "url", "created", "doc")
    for i, leaf in enumerate(leaves):
        data = leaf.data
        # 过滤掉公司内部网站
        if "gridsum" in data.url:
            continue

        # 下载
        try:
            html = download(data.url)
        except Exception as e:
            print("下载: %s(%s)发生异常: %s" % (leaf.name, data.url, e))
            continue

        # 解析
        try:
            text = extract_text(html)
            if len(bytes(text, encoding="utf-8")) > 65535:
                print("网站: %s内容超出65535个字符" % data.url)
                continue
        except Exception as e:
            print("解析: %s(%s)发生异常: %s" % (leaf.name, data.url, e))
            continue

        print("成功下载并解析: ", data.url)
        dataset.append((leaf.name, data.url, data.created, text))

    try:
        save(dataset)
    except Exception as e:
        print("保存到数据库发生异常: %s" % e)
    else:
        print("保存%s条数据到数据库" % len(dataset))


def main():
    root_element = visit(root)
    leaves = root_element.get_leaves()
    # 控制同时运行的线程为8
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        index, step = 0, 10
        while index < len(leaves):
            tmp = leaves[index: index + step]
            index = index + step
            executor.submit(download_and_save, tmp)


if __name__ == "__main__":
    main()
