import random
import re
from threading import Thread, Lock

import requests
import schedule
from bs4 import BeautifulSoup

from utils import flatten

lock1 = Lock()


def get_ip_table(url_b):
    # print("get_ip_table: ", url_b)
    res = requests.get(url_b)
    # print(res.content)
    soup = BeautifulSoup(res.content, "html.parser")
    trs = soup.find_all("tr")
    op_list = []
    for i in trs:
        # print("in...")
        tds = i.find_all("td")
        dd = []
        for j in tds:
            dd.append(j.text.strip())
        if len(dd) >= 2:
            # print("ininin....")
            _ip = dd[0]
            _port = dd[1]
            op_list.append((_ip, _port))
            # print(_ip, _port)
    return op_list


class IpTool:
    def init(self, filename=None):
        self.proxy_list = []
        if filename is not None:
            self.load_from_file(filename)
        else:
            self.generators.append(self.__get_from_89__)
            # self.generators.append(self.__get_from_89_by_api)
            self.generators.append(self.__get_from_kdl__)
            self.generators.append(self.__get_from_ydl__)
            for fun in self.generators:
                print("gen->", fun.__name__)
                ops = fun()
                print("ops len:", len(flatten(ops)))
                self.test_generator(ops)

    def __init__(self, filename=None):
        self.proxy_list = []
        self.test_proxy_list = []
        self.generators = []
        self.HAVE_SAVE = False
        self.init(filename)

    def test_all(self, ip_list=None):
        if ip_list is None:
            ip_list = self.test_proxy_list

        ls = flatten(ip_list)
        # print(ls)
        thread_list = []
        for it in ls:
            thread_list.append(Thread(target=self.__test__, args=(it[0], it[1])))
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for t in thread_list:
            t.join(timeout=15)
        print("TEST DONE!")

    def __test__(self, ip, port):
        lock1.acquire()
        print("test..", ip, ":", port)
        lock1.release()
        test_url = "http://httpbin.org/get"
        try:
            res = requests.get(test_url, proxies=self.get_proxy(ip, port), timeout=10)
            if res.status_code == 200:
                self.proxy_list.append((ip, port))
        except:
            pass

    def test_generator(self, ls):
        l1 = len(self.proxy_list)
        self.test_all(ls)
        l2 = len(self.proxy_list)
        print("From {} get {}".format(len(flatten(ls)), l2 - l1))

    def save_to_file(self, filename="ips.txt"):
        print("save out...")
        with open(filename, "w+") as f:
            print("save...")
            for item in self.proxy_list:
                f.write(item[0] + "\t" + item[1] + "\n")

    def load_from_file(self, filename="ips.txt"):
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                ip, port = line.split("\t")
                self.proxy_list.append((ip, port))

    def __delitem__(self, key):
        self.delete(key)

    def delete(self, key):
        self.proxy_list.remove(key)

    @staticmethod
    def __get_from_xici__():
        pass

    @staticmethod
    def __get_from_ydl__():
        url = "http://www.ip3366.net/?stype=1&page="
        ip_port_list = []
        for index in range(1, 11):
            ip_port_list.append(get_ip_table(url + str(index)))

        return ip_port_list

    @staticmethod
    def __get_from_kdl__():
        print("kdl......")
        url1 = "https://www.kuaidaili.com/free/inha/"
        url2 = "https://www.kuaidaili.com/free/intr/"
        ip_port_list = []

        for index in range(1, 11):
            ip_port_list.append(get_ip_table(url1 + str(index)))
            ip_port_list.append(get_ip_table(url2 + str(index)))

        return ip_port_list

    @staticmethod
    def __get_from_89__():
        print("__get_from_89__")
        url = "https://www.89ip.cn/index_"
        ip_port_list = []

        for index in range(1, 31):  # 只爬前30页的
            ip_port_list.append(get_ip_table(url + str(index) + ".html"))
            index += 1

        return ip_port_list

    @staticmethod
    def __get_from_89_by_api():
        r = re.compile("[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}:[0-9]{1,4}")
        url = "http://api.89ip.cn/tqdl.html?api=1&num=600&port=&address=&isp="
        grps = r.findall(str(requests.get(url).content))
        res = []
        for g in grps:
            # print(g)
            ip, port = g.split(":")
            res.append((ip, port))
        return [res]

    def random(self):
        return random.choice(self.proxy_list)

    def get_all(self):
        return self.proxy_list

    def get_proxy(self, ip, port):
        proxies = {
            'http': 'http://' + ip + ":" + port,
            'https': 'https://' + ip + ":" + port
        }
        return proxies

    def get_random_proxy(self):
        ip, port = self.random()
        return self.get_proxy(ip, port)


if __name__ == "__main__":
    IPT = IpTool()
    schedule.every(5).minutes.do(IPT.init)
    while True:
        schedule.run_pending()
