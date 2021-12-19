import datetime
import re
import time

import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from answer.answer import CodeAnswer
from utils import send_message
from autoacspider.spider import *


class DotCppSpider(Spider):
    db_name = "dotcpp"
    account = "2020ffgz"
    password = "20202020"
    has_login = False
    tasks = []

    def __init__(self, pidlist=None, l=None, r=None):
        Spider.__init__(self)
        self.bs = webdriver.Chrome()
        self.mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.has_passed = self.get_haspassed()
        if pidlist is not None:
            self.tasks = pidlist
        if l is not None and r is not None:
            for pid in range(int(l), int(r) + 1):
                self.tasks.append(pid)

    def run(self):
        ok_pid = self.get_okpid()
        print(ok_pid)
        print(type(ok_pid[0]))
        for pid in self.tasks:
            if str(pid) in ok_pid:
                continue
            try:
                self.AC(pid, "C++")
            except:
                _time = datetime.datetime.now().strftime("%m-%d_%H:%M")
                subject = "发生错误@" + _time
                msg = subject
                send_message(msg=msg, subject=subject, receiver="3282174135@qq.com")
                time.sleep(30)
                continue

    def AC(self, pid, _type="C++"):
        if not self.has_login:
            self.log_in()

        ans_list = self.load_answer(pid, _type)

        if ans_list is None or len(ans_list) == 0:
            print("try.......")
            try:
                _list = self.get_url_list(pid)
            except:
                _list = self.get_url_list(pid)
            cnt = 0
            for ans in _list:
                # print(ans)
                print("为{}({})尝试第{}次".format(pid, _type, cnt))
                cnt += 1
                try:
                    self.get_code(ans)
                except:
                    self.get_code(ans)
                if settings.IGNORE_CODE_TYPE or ans._type == _type:
                    self.push_code(ans)
                    if self.get_answer_status():
                        # print(ans)
                        print(ans.save_to_mongodb(self.db_name))
                        break
                    else:
                        ans.save_wrong()
        else:
            print("db.......")
            ans = ans_list[0]
            self.push_code(ans)

    def load_answer(self, pid, _type="C++"):
        print(pid, _type)
        ans_list = []
        db = self.mongoclient[self.db_name]
        col = db[str(pid)]
        if settings.IGNORE_CODE_TYPE:
            rows = col.find()
        else:
            rows = col.find({"type": _type})
        for ans in rows:
            del ans["_id"]
            ans_list.append(CodeAnswer(ans))
        return ans_list

    def push_code(self, ans):
        pid, code_str, code_type = ans.pid, ans.code, ans._type
        url = "https://www.dotcpp.com/oj/problem{}.html".format(pid)
        try:
            self.bs.get(url)
            self.wait()
            # 更改默认语言
            s1 = Select(self.bs.find_element_by_id("lang_chose"))
        except:
            try:
                self.bs.get(url)
                # 更改默认语言
                self.wait()
                s1 = Select(self.bs.find_element_by_id("lang_chose"))
            except:
                return False

        _type = ["C", "C++", "JAVA", "Python", "PHP"]
        _index = _type.index(code_type)
        s1.select_by_index(_index)

        # 找到text标签
        text = self.bs.find_element_by_xpath("//*[@id=\"editor\"]/textarea")
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
        self.wait(3, 5)
        button = self.bs.find_element_by_xpath("//*[@id=\"tijiao\"]")

        try:
            button.click()
        except:
            button = self.bs.find_element_by_xpath("//*[@id=\"tijiao\"]")
            self.wait(3, 5)
            button.click()
        self.wait()

    def get_answer_status(self):
        self.bs.refresh()
        self.wait(3, 5)
        status = []
        try:
            status = self.bs.find_elements_by_class_name("evenrow")
            status = status[0].find_elements_by_class_name("btn-success")
        except:
            return False

        if len(status) == 0:
            return False
        else:
            return True

    def get_url_list(self, pid):
        page, url_cnt = 1, -1
        _list = []
        while url_cnt != 0:
            self.wait(1, 2)
            url = "https://blog.dotcpp.com/tijie/p{}/?page={}".format(pid, page)
            soup = BeautifulSoup(requests.get(url, headers=self.random_header(pid=pid)).content, "html.parser")
            urls = soup.find_all("a", class_="list_title")
            url_cnt = len(urls)
            for it in urls:
                ans = CodeAnswer()
                ans.pid = pid
                ans.url = it.get("href")
                ans._type = re.search("Python|C\+\+|JAVA|C|PHP", it.next_sibling.next_sibling.text).group()
                _list.append(ans)
            print("从第{}页拿到{}条链接".format(page, url_cnt))
            page += 1
        return _list

    def get_code(self, answer, depth=1):
        print("code...")
        try:
            url = "https://blog.dotcpp.com{}".format(answer.url)
            soup = BeautifulSoup(
                requests.get(url, headers=self.random_header(tjpid=answer.pid), proxies=self.random_proxy(),
                             timeout=15).text,
                'html.parser')
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

            if code_str is None:
                # 无法提取代码的页面
                return False

            # 对代码进行处理
            answer.code = code_str
            code_str = self.format_code(answer, pro_type)
            answer.code = code_str
            return code_str
        except:
            if depth >= 10:
                return None
            return self.get_code(answer, depth + 1)

    def format_code(self, ans, pro_type):
        code = ans.code
        wchr = [160, 13]
        for it in wchr:
            code = code.replace(chr(it), " ")  # nbsp
        code = code.replace(chr(9), "")
        code = re.sub("[\u4e00-\u9fa5]", "", code, re.M)  # 中文
        code = re.sub("//.*$", " ", code, re.M)  # 注释
        # code = re.sub("(?<!>)>(?!>)", ">\n", code, re.M)  # 对于前面后都不是>的>后面加一个换行
        code = re.sub("^[\s]{1,}", "", code, re.M)  # 去除行首空白字符
        try:
            if "C" in ans._type:
                code = re.search("#include.*}", code, re.A).group()
                if pro_type == 2:
                    code = re.sub("#include", "", code)
                    code = "#include<bits/stdc++.h>\n" + code
        except:
            pass
        return code

    def log_in(self):
        url = "https://www.dotcpp.com/oj/loginpage.php"
        self.bs.get(url)
        account = input("请输入账号:")
        password = input("请输入密码:")
        captcha = input("请输入验证码:")
        if len(account) > 2:
            self.account = account
        if len(password) > 2:
            self.password = password
        self.wait()
        # self.wait()  # 找到账号框并输入账号 H1810317091 20202020a 2020ffgz  H1910823009
        self.bs.find_element_by_name('user_id').send_keys(self.account)
        # self.wait()  # 找到密码框并输入密码 dotpork2020 2020porka 20202020  a62651757
        self.bs.find_element_by_name('password').send_keys(self.password)
        # self.wait()  # 找到验证码框并输入验证码

        self.bs.find_element_by_name('vcode').send_keys(captcha)
        self.wait()  # 找到登陆按钮并点击
        self.bs.find_element_by_id('tijiao').click()
        self.has_login = True
        self.wait()

    def get_haspassed(self, account=None):
        if account is None:
            account = self.account
        url = "https://www.dotcpp.com/home/{}".format(account)
        res = requests.get(url, headers=self.random_header())
        _list = []
        grps = re.findall("p\(([0-9]{4})\)", res.text)
        for i in grps:
            _list.append(int(i))
        return _list

    def wait(self, a=1, b=3):
        time.sleep(random.randint(a, b))

    def get_okpid(self):
        mgc = pymongo.MongoClient("mongodb://localhost:27017/")
        dotdb = mgc["dotcpp"]
        ll = dotdb.list_collection_names()
        return [i for i in ll]


if __name__ == "__main__":
    ans = CodeAnswer()
    ans.url = "/a/7976"
    ans.pid = 1207
    spider = DotCppSpider()
    res = spider.get_code(ans)
    print(res)
