import threading

from flask import Flask

import iptool
import settings

__all__ = ['app']
app = Flask(__name__)


def init():
    settings.API_UPDATING = True
    global IPT
    IPT = iptool.IpTool()
    settings.API_UPDATING = False


@app.route('/')
def index():
    return "Hi,Welcome!</br><a href=\"/random\">获取随机代理</a>"


@app.route("/random")
def get_proxy():
    return IPT.get_random_proxy()


if __name__ == "__main__":
    init()
    timer = threading.Timer(60 * 5, init)
    timer.start()
    app.run()
