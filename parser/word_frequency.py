import jieba.posseg as pseg
from collections import Counter
import os
import requests
from datetime import datetime
import time
from .config import DIR_PATH, STOP_WORDS_FILE

POS_FILTER = ["n", "v", "vn"]


def get_stop_words(file_path):
    with open(file_path) as f:
        result = f.readlines()
        result = [r for r in result if r.strip()]
        return result


def get_word_frequency(text):
    stop_words = get_stop_words(os.path.join(DIR_PATH, STOP_WORDS_FILE))
    words = pseg.cut(text)
    eng_words = [word for word, flag in words if flag == "eng"]
    eng_words_frequency = get_word_frequency_from_api(' '.join(eng_words))
    chinese_words = [word for word, flag in words if flag in POS_FILTER and len(word) > 1 and word not in stop_words]
    counter = Counter()
    for word, flag in chinese_words:
        counter[word] += 1
    return counter + eng_words_frequency


def get_word_frequency_from_api(text):
    url = "http://corenlp.run/"
    properties = '{"annotators":"tokenize,ssplit,pos", "date": "%s", "outputFormat":"json"}' % datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    params = {"properties": properties, "pipelineLanguage": "en"}
    result = requests.post(url, data=text.encode("utf-8"), params=params)
    if result.status_code != 200:
        print("错误码: %s, 响应内容: %s" % (result.status_code, result.content))
        print("文档内容: %s\n" % text)
        return Counter()
    sentences = result.json()["sentences"]
    counter = Counter()
    print("句子个数: %s" % len(sentences))
    for sentence in sentences:
        for token_info in sentence["tokens"]:
            word = token_info["word"]
            pos = token_info["pos"]
            if pos.startswith("N") or pos.startswith("V"):
                counter[word] += 1
    time.sleep(0.5)
    return counter


if __name__ == "__main__":
    text = """| 云风的 BLOG
思绪来得快去得也快，偶尔会在这里停留
January 31, 2019
设计了一个数据格式
最近一段时间在忙着设计和实现我们游戏引擎用到的数据格式。
在此之前，我们一直在直接使用 lua 描述数据；但最近随着数据类型系统的完善，同事建议设计一种专有数据格式会更好。希望专用格式手写和阅读起来能比 lua 方便，对 diff 更友好，还能更贴近我们的类型系统，同时解析也能更高效一些。lua 的解析器虽然已经效率很高，但是在描述复杂数据结构时，它其实是先生成的构造数据结构的字节码，然后再通常虚拟机运行字节码才构造出最终的数据结构。这样的两步工作会比一趟扫描解析构造要慢一些且消耗更多的内存。
现有的流行数据格式都有一些我们不太喜欢的缺点：
阅读全文 "设计了一个数据格式" »
云风 提交于 09:29 AM
|
固定链接
留言 (14)
January 09, 2019
粒子系统的设计
因为需要为我们的 3d engine 添加特效系统的模块，我最近读了一篇文章：
Efficient CPU Particle Systems
文章很长，夹杂着设计思路，优化，算法实现，渲染实现。对于我来说，由于过去我做过好几版粒子系统，所以读起来不太费力，很多细节可以直接略过，我今天写一篇 blog 把我认为文章中对我最有参考价值的部分列出来。
阅读全文 "粒子系统的设计" »
云风 提交于 03:25 PM
|
固定链接
留言 (8)
January 08, 2019
一种 16 倍抗锯齿字体渲染的方法
昨天读了几篇文章，讲解了
一种新的抗锯齿字体渲染的方法
我觉得颇有意思，就
试着实现了一版 CPU 版本
阅读全文 "一种 16 倍抗锯齿字体渲染的方法" »
云风 提交于 03:38 PM
|
固定链接
留言 (10)
December 18, 2018
lua 5.4 可能会增加 to-be-closed 特性
如果你有关注 lua 在 github 上的仓库，就会发现，最近一段时间增加了一个新特性：to-be-closed 的 local 变量。
鉴于历史上 lua 每次的大版本开发过程中都会增加很多有趣的特性，却无法保持到版本正式发布。本文也只是介绍一下这个有趣的特性，并不保证它一定会被纳入语言标准。正式的发布版中即使有这个特性，语法上也可能有所不同。
我认为 Lua 加入这个特性的动机是它缺乏 RAII 机制。过去，我们必须用 pcall 来确保一段代码运行完毕，然后再清理相关的资源。这会导致代码实现繁琐，几乎无法正确实施。比如，如果你用 C 函数申请了一块资源，期望在使用完毕后可以清除干净，过去就只能依赖 __gc 方法。但 gc 的时机不可控，往往无法及时清理。如果你把释放过程放在运行过程的末尾，是很难确定整个运行过程中没有异常跳出的可能，那样就无法执行最后的释放流程。
阅读全文 "lua 5.4 可能会增加 to-be-closed 特性" »
云风 提交于 10:15 AM
|
固定链接
留言 (4)
December 03, 2018
惰性编译资源仓库中的源文件
我们的 3d engine 的资源仓库使用
Merkle tree
好几篇 blog
现阶段已完成的版本，已经做到把 lua 虚拟机和所有 C/C++ 实现的 lua 库静态编译打包为一个执行文件，可以零配置启动运行，通过网络远程访问一个 vfs 仓库，完成自举更新和运行远程仓库里的项目。
最近在开发的过程中，发现了一点 Merkle tree 的局限性，我做了一些改进。
阅读全文 "惰性编译资源仓库中的源文件" »
云风 提交于 10:45 AM
|
固定链接
留言 (3)
November 30, 2018
ECS 中的 Entity
我认为 ECS 框架针对的问题是传统面向对象框架中，对象数量很多而对象的特性非常繁杂，而针对对象的不同方面 aspect 编写处理逻辑会非常繁杂。每个针对特定的方面执行业务，都需要从众多对象中挑选出能够操作的子集，这样性能低下，且不相关的特性间耦合度很高。
所以 ECS 框架改变了数据组织方式，把同类数据聚合在一起，并用专门的业务处理流程只针对特定数据进行处理。这就是 C 和 S 的概念：Component 就是对象的一个方面 aspect 的数据集，而 System 就是针对特定一个或几个 aspect 处理方法。
那么，Entity 是什么呢？
我认为 Entity 主要解决了三个问题。
阅读全文 "ECS 中的 Entity" »
云风 提交于 03:08 PM
|
固定链接
留言 (9)
November 21, 2018
3d engine 项目招聘
我们的 3d engine 项目从 2018 年 1 月底开始，已经过去 10 个月了。比原计划慢，但是进度还可以接受。目前已经大致完成了运行时的基础渲染框架（基于 ecs 模式），整合了 bullet 物理引擎，开发了一个基于网络的虚拟文件系统，可以不依赖本地的资源/代码直接远程运行。另外还开发了一个 lua 的远程交互调试器，可提升 lua 的开发效率。
单从 runtime 角度，引擎的完成度已经较高。但和之前开发 ejoy2d 不同，这次希望把引擎的侧重点放在工具链上。所以虽然有计划开源，但在工具链不成熟的现阶段，暂时还是闭源开发。
目前团队有全职程序 3 名，我个人没有全职加入，但也花了颇多精力在上面。所以在关键节点上，我们已有 4 个人全力开发。
现在想再招聘一名成员，主要想补充工具链，尤其是开发环境/编辑器的开发。让引擎可以在半年内可用于新游戏 demo 的开发。对于这个职位，可以列出下列明确的需求：
阅读全文 "3d engine 项目招聘" »
云风 提交于 05:01 PM
|
固定链接
留言 (13)
Misc
留言本
用 email 联系我
Github
我不用微信
我不用 QQ
Search
Categories
读书
概率与桥牌
技术
Erlang
Go 语言
Unix
Windows
X Window
build tool
lua与虚拟机
skynet
调试
算法
网络与安全
优化与技巧
语言与设计
随笔
《我的编程感悟》
游戏
游戏开发
桌面游戏
杂记
Google
简悦
攀岩
网易
我爱折腾
"""
    get_word_frequency_from_api(text)
