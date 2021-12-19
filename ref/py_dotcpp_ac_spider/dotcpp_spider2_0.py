import random
import re as r
import time

import requests as re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


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

    # 统一处理  注释   傻逼空格
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
    flag = 0
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


def login():
    # # 获取验证码图片
    url = "https://www.dotcpp.com/oj/loginpage.php"
    bs.get(url)
    sleep()

    # sleep()  # 找到账号框并输入账号 H1810317091 20202020a 2020ffgz  H1910823009
    bs.find_element_by_name('user_id').send_keys("2020ffgz")
    # sleep()  # 找到密码框并输入密码 dotpork2020 2020porka 20202020  a62651757
    bs.find_element_by_name('password').send_keys("20202020")
    # sleep()  # 找到验证码框并输入验证码
    captcha = input("请输入验证码")
    bs.find_element_by_name('vcode').send_keys(captcha)
    sleep()  # 找到登陆按钮并点击
    bs.find_element_by_id('tijiao').click()


def pushCode(str, code):
    url = "https://www.dotcpp.com/oj/problem" + str + ".html"
    bs.get(url)
    sleep()

    # 更改默认语言
    try:
        s1 = Select(bs.find_element_by_id("lang_chose"))
        s1.select_by_index(1)
    except:
        return False

    # 找到text标签
    text = bs.find_element_by_xpath(
        "//*[@id=\"editor\"]/textarea")
    # 全选并清空文本
    text.send_keys(Keys.CONTROL, 'a')
    text.send_keys(Keys.BACK_SPACE)
    sleep()
    text.send_keys(code)

    text.send_keys(Keys.SPACE, Keys.SPACE, Keys.SPACE, Keys.SPACE, Keys.SHIFT, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                   Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                   Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                   Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN)
    text.send_keys(Keys.BACK_SPACE)
    sleep()
    # 点击提交
    button = bs.find_element_by_xpath(
        "//form[@action='submit.php']//button[@type='button']")

    button.click()
    time.sleep(4)
    bs.refresh()
    sleep()
    status = bs.find_elements_by_class_name("evenrow")

    status = status[0].find_elements_by_class_name("btn-success")

    if len(status) == 0:
        return False
    else:
        return True


def AC(num):
    try:
        title_arr = getTitle(str(num))
        for title in title_arr:
            code = getCode(title)
            if not code:
                continue
            status = pushCode(num, code)
            if not status:
                continue
            break
    except:
        return False


able = []
bs = webdriver.Chrome()
login()
for i in range(1000, 2400):
    AC(str(i))

'''
日志:
dotcpp_spider2.0
完成时间:2020-11-29
效果:C语言网共1400道题成功AC940道
使用账号:1. 20202020a   2020porka
        2. 2020ffgz    20202020
改进方向:
1. 获取首页已A题目列表 自动跳过已过的题目
2. 存储成功A题的博客索引 以后可以直接取 不用再一个个尝试
3. 对部分博客内容还是没做适配 感觉极限可以上1200
4. 效率过低  可以尝试结合多线程重构爬虫

'''
