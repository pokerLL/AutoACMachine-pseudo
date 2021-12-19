import json
import random

import requests
from faker import Faker

import settings

referers = [
    "https://www.dotcpp.com/wp/",
    "https://blog.dotcpp.com/",
    "https://www.dotcpp.com/oj/problemset.html"
]
header = {
    "accept": "text/html",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "referer": "",
    "user-agent": "",
}


class Spider:

    def __init__(self, need_proxy=False):
        self.fk = Faker()

    def random_header(self, pid=None, tjpid=None):
        if not settings.NEED_RANDOM_HEADER:
            return None

        if pid is not None:
            header["referer"] = "https://www.dotcpp.com/oj/problem{}.html".format(pid)
        elif tjpid is not None:
            header["referer"] = "https://blog.dotcpp.com/tijie/p{}/".format(pid)
        else:
            header["referer"] = random.choice(referers)
        header["user-agent"] = self.fk.user_agent()
        return header

    def random_proxy(self):
        if not settings.NEED_RANDOM_PROXY or settings.API_UPDATING:
            return None

        res = requests.get(settings.WEB_API_URL)
        return json.loads(res.text)
