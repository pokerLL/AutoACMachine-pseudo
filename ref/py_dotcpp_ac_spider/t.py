import random
import re as r
import time

import requests as re
from bs4 import BeautifulSoup


def sleep():
    time.sleep(random.randint(1, 3))


def getTitle(num):
    url = "https://blog.dotcpp.com/tijie/p" + num + "/"
    res = re.get(url)
    sleep()
    res.encoding = 'utf8'
    if res.status_code != 200:
        return False

    soup = BeautifulSoup(res.text, "html.parser")
    divs = soup.find_all("a", class_="list_title")
    tit_arr = []
    for item in divs:
        if "C" in item.find_next_sibling("span", class_="list_normal").get_text():
            tit_arr.append(item["href"])
    return tit_arr


def proCode(code_div):
    code = r.search("#include[ ]?[\s\S]*}", code_div)
    try:
        code = code.group()
    except:
        return False

    # 统一处理  注释   空格
    code = r.sub("\u00A0", " ", code)
    code = r.sub("(\240|\302)", " ", code)
    code = r.sub("[\t]?", "", code)
    code = r.sub("[ ]{2,}", "", code)
    if r.search('#include[ ]?(<|")[\s\S]*(>|")', code) is None:  # 头文件缺失 textarea
        # print("进入处理模式1")
        code = r.sub("#include", "", code)
        code = "#include<bits/stdc++.h>\n" + code
    else:  # 正常代码 pre
        # print("进入处理模式2")
        pass
    return code


def getCode(str):
    try:
        url = "https://blog.dotcpp.com" + str
    except:
        return False

    header = {
        'DNT': '1',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
        "Content-Type": "text/css"
    }

    res = re.get(url, headers=header)

    sleep()

    res.encoding = 'utf8'
    if res.status_code != 200:
        return False

    soup = BeautifulSoup(res.text, 'html.parser')
    divs = soup.find_all("pre", class_=r.compile("toolbar"))
    if len(divs) == 0:
        divs = soup.find_all("div", class_="blog_content")
        divs = divs[0].find_all("textarea")
    if len(divs) == 0:
        return False

    code_div = divs[0].getText()
    code = proCode(code_div)
    return code


def AC(num):
    try:
        title_arr = getTitle(str(num))
        for title in title_arr:
            code = getCode(title)
            if code:
                break
    except:
        return False


able = []

for i in range(1000, 2400):
    AC(str(i))

'''
日志:
dotcpp_spider2.0
完成时间:2020-11-29
效果:C语言网共1400道题成功AC940道
使用账号:1. 20202020a   2020porka
        2. 2020ffgz    20202020

'''
