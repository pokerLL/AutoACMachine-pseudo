import json
import os
import random
import re
import time
from collections import namedtuple

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import iptool

CodeAnswer = namedtuple("CodeAnswer", "pid type url code")


class Spider:

    def __init__(self):
        self.ipt = iptool.IpTool()
        self.ipt.load_from_file()

    def random_header(self):
        pass

    def random_proxiy(self):
        ip, port = self.ipt.random()
        proxies = self.ipt.getprox(ip, port)
        return proxies


class DotCppSpider(Spider):
    account = "2020ffgz"
    password = "20202020"
    invaild_url_list = []
    has_passed = []
    answers = {}
    tj_type = {}
    mark_pid_type = {}
    has_login = False

    def __init__(self):
        Spider.__init__(self)
        self.bs = webdriver.Chrome()
        self.AC_range(1000, 1020)
        self.save(dirname="ANS", filename="answers.json")
        # print(self.answers)

    def login(self):
        # # 获取验证码图片
        url = "https://www.dotcpp.com/oj/loginpage.php"
        self.bs.get(url)
        self.wait()

        # self.wait()  # 找到账号框并输入账号 H1810317091 20202020a 2020ffgz  H1910823009
        self.bs.find_element_by_name('user_id').send_keys(self.account)
        # self.wait()  # 找到密码框并输入密码 dotpork2020 2020porka 20202020  a62651757
        self.bs.find_element_by_name('password').send_keys(self.password)
        # self.wait()  # 找到验证码框并输入验证码
        captcha = input("请输入验证码")
        self.bs.find_element_by_name('vcode').send_keys(captcha)
        self.wait()  # 找到登陆按钮并点击
        self.bs.find_element_by_id('tijiao').click()

    @staticmethod
    def wait(a=1, b=3):
        time.sleep(random.randint(a, b))

    def AC_range(self, a, b):
        for it in range(int(a), int(b) + 1):
            self.AC_new(it)

    def AC_new(self, pid):
        if not self.has_login:
            self.login()
            self.has_login = True

        url_list = self.get_tj_urls(pid)
        for url in url_list:
            mk_key = str(pid) + self.tj_type[url]
            if mk_key in self.mark_pid_type:
                print(mk_key, "  hit..")
                continue
            else:
                print(mk_key, "  load..")

            code_str = self.get_tj_code(url)
            _answer = CodeAnswer(pid=pid, url=url, type=self.tj_type[url], code=code_str)
            if pid not in self.answers:
                self.answers[pid] = []
            if self.push_code(pid, code_str, self.tj_type[url]):
                self.answers[pid].append(_answer)
                self.mark_pid_type[mk_key] = True
            else:
                self.invaild_url_list.append(url)

    def push_code(self, pid, code_str, code_type):
        url = "https://www.dotcpp.com/oj/problem{}.html".format(pid)
        self.bs.get(url)
        # 更改默认语言
        try:
            s1 = Select(self.bs.find_element_by_id("lang_chose"))
            # s1.select_by_value(code_type)
            if code_type == "C":
                s1.select_by_index(0)
                pass
            elif code_type == "C++":
                s1.select_by_index(1)
                pass
            elif code_type == "JAVA":
                s1.select_by_index(2)
                pass
            elif code_type == "Python":
                s1.select_by_index(3)
                pass
            elif code_type == "PHP":
                s1.select_by_index(4)
                pass

        except:
            return False

        # 找到text标签
        text = self.bs.find_element_by_xpath(
            "//*[@id=\"editor\"]/textarea")
        # 全选并清空文本
        text.send_keys(Keys.CONTROL, 'a')
        text.send_keys(Keys.BACK_SPACE)
        self.wait()
        text.send_keys(code_str)

        text.send_keys(Keys.SPACE, Keys.SPACE, Keys.SPACE, Keys.SPACE, Keys.SHIFT, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                       Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                       Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                       Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN)
        text.send_keys(Keys.BACK_SPACE)
        self.wait(4, 7)
        # 点击提交
        button = self.bs.find_element_by_xpath("//*[@id=\"tijiao\"]")
        self.wait(4, 7)
        try:
            button.click()
        except:
            self.wait(4, 7)
            button.click()
        self.wait()
        self.bs.refresh()
        self.wait()
        status = self.bs.find_elements_by_class_name("evenrow")

        status = status[0].find_elements_by_class_name("btn-success")

        if len(status) == 0:
            return False
        else:
            return True

    def get_tj_urls(self, pid):
        url = "https://blog.dotcpp.com/tijie/p{}/".format(pid)
        res = requests.get(url, headers=self.random_header(), proxies=self.random_proxiy())

        soup = BeautifulSoup(res.content, 'html.parser')
        urls = soup.find_all("a", class_="list_title")
        url_list = []
        for it in urls:
            tj_url = it.get("href")
            url_list.append(tj_url)
            tj_type = re.search("Python|C\+\+|JAVA|C|PHP", it.next_sibling.next_sibling.text).group()
            self.tj_type[tj_url] = tj_type
        return url_list

    def get_tj_code(self, tj_url):
        url = "https://blog.dotcpp.com{}".format(tj_url)
        res = requests.get(url, headers=self.random_header(), proxies=self.random_proxiy())

        soup = BeautifulSoup(res.text, 'html.parser')

        pro_type = 1

        try:
            # 第一种 直接pre内
            code_div = soup.find("pre", class_=re.compile("toolbar"))
            code_str = code_div.text
        except AttributeError:
            # 第二种 在textarea内
            try:
                pro_type = 2
                code_div = soup.find("textarea", style=re.compile("display:none"))
                code_str = code_div.text
            except:
                pro_type = 3
                code_div = soup.find("div", class_="ueditor_container")
                code_str = code_div.text

            # code_div = soup.find("div", class_="ueditor_container")

        if code_str is None:
            # 大部分代码都可以被提取出来
            self.invaild_url_list.append(url)

        # 对代码进行处理
        code_str = self.pro_code(code_str, pro_type)

        # self.code_str[tj_url] = code_str
        return code_str

    def pro_code(self, code_str, tj_type):
        code = code_str
        if type(code) is None:
            return
        code = code.replace(chr(160), " ")  # nbsp
        code = code.replace(chr(13), "")  # 空行
        code = re.sub("[\u4e00-\u9fa5]", "", code, re.M)  # 中文
        code = re.sub("//.*$", " ", code, re.M)  # 注释
        code = re.sub(">", ">\n", code, re.M)
        try:
            code = re.search("#incl[\S\s]*}", code).group()
            if tj_type == 2:
                code = re.sub("#include", "", code)
                code = "#include<bits/stdc++.h>\n" + code
        except:
            pass

        return code

    def get_haspassed(self, account):
        url = "https://www.dotcpp.com/home/{}".format(account)
        res = requests.get(url, headers=self.random_header(), proxies=self.random_proxiy())

        grps = re.findall("p\(([0-9]{4})\)", res.text)
        for i in grps:
            self.has_passed.append(int(i))

    def save(self, dirname, filename):
        if filename is None:
            self.save_to_mongodb()
        else:
            self.save_to_file(dirname, filename)
        pass

    def save_to_file(self, dirname, filename):
        try:
            os.mkdir(dirname)
        except:
            pass
        os.chdir(dirname)

        print(self.answers)
        with open(filename, "w+") as f:
            json.dump(self.answers, f)
        # print(self.answers)

    def save_to_mongodb(self):
        pass

    def load(self, dirname, filename):
        if filename is None:
            self.load_from_mongodb()
        else:
            self.load_from_file(dirname, filename)
        pass

    def load_from_file(self, dirname, filename):
        with open(dirname + "/" + filename, "r") as f:
            self.answers = json.load(f)

    def load_from_mongodb(self):
        pass
