import datetime

from autoacspider.dotcppspider import DotCppSpider
from utils import send_message


def menu():
    pass


def cho_set():
    pass


def choose_site():
    chostr = '''
    1.dotcpp\n
    '''
    return int(input(chostr))


def choose_mode():
    chostr = '''
    1. one by one(quit by input -1)
    2. input a range
    '''
    return int(input(chostr))


def mode_1():
    inpstr = '''
    请一个个输入题号，并以空格间隔：
    '''
    print(inpstr)
    ls = list(input().split(" "))
    return ls


def mode_2():
    inpstr = '''
    请输入要AC的题目区间，并以空格间隔：
    '''
    l, r = input(inpstr).split(" ")
    return l, r


if __name__ == "__main__":
    # site = choose_site()
    # mode = choose_mode()
    # spider = None
    # if mode == 1:
    #     ls = mode_1()
    #     spider = DotCppSpider(pidlist=ls)
    # else:
    #     l, r = mode_2()
    #     spider = DotCppSpider(l=int(l), r=int(r))
    spider = DotCppSpider(l=2045, r=2640)
    print(spider.tasks)
    try:
        spider.run()
    except:
        time = datetime.datetime.now().strftime("%m-%d_%H:%M")
        msg = "发生错误@" + time
        send_message(msg=msg, subject=msg, receiver="3282174135@qq.com")
