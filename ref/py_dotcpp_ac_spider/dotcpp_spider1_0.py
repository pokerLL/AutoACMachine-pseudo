import requests as re
from lxml import etree
import re as r
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select


def sleep():
    time.sleep(random.randint(1, 2))


def getTitle(num):

    # print("开始爬取文章列表")
    url1 = "https://blog.dotcpp.com/tijie/p"+num+"/"
    # print(url1)
    res = re.get(url1)
    sleep()
    res.encoding = 'utf8'
    if res.status_code != 200:
        print("SOMTHING WRONG --!200")
        return False
    dom = etree.HTML(res.text)
    par_list = dom.xpath(
        '//tr/td/a[@class="list_title" and @href and @target="_blank"]')

    # print("文章列表爬取成功")
    for i in par_list:
        if 'C' in i.xpath('string(.)'):
            tit = i.xpath('@href')[0]
            # print(tit)
            return tit


def getCode(str):
    flag = 0
    try:
        url = "https://blog.dotcpp.com"+str
    except:
        return False
    # print(url)
    header = {
        'DNT': '1',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36'
    }

    res = re.get(url, headers=header)

    sleep()

    res.encoding = 'utf8'
    if res.status_code != 200:
        return "SOMTHING WRONG --!200"

    # f = open("F:/1.txt",'w+')
    # f.write(res.text)

    soup = BeautifulSoup(res.text, 'html.parser')

    divs = soup.find_all('pre', class_=r.compile(
        "brush"), string=r.compile("#include"))

    if len(divs) != 0:
        flag = 1
    if flag == 0:
        # divs = soup.find_all('textarea', string=r.compile("#include"))#style_=r.compile("display")
        divs = soup.find_all('div', class_=r.compile("blog_content"))
        flag = 2
    if len(divs) == 0:
        flag = 0
    if flag == 0:
        return False

    code_div = divs[0].getText()
    try:
        code_div = r.search("#include[\w\s\S]*}", code_div).group()
    except:
        return False

    # 处理疑难杂症
    code = ""
    if flag == 2:
        code = r.sub("#include[ ]*[^\<]", "", code_div)
        code = r.sub("<[a-z]*>", "", code)
        if code.find("#include") == -1:
            code = "#include<bits/stdc++.h>\n"+code
    else:
        code = r.search("#include[\w\s\S]*}", code_div).group()

    code = r.sub("\u00A0", " ", code)
    f = code.split("\n")
    if len(f) == 1:
        code = r.sub("[ ]{3,}", "\n", code)
        return code

    code = r.sub("[ ]{2,}", "", code)
    code = r.sub("[\t]?", "", code)
    code = r.sub("//[\S]*", "", code)
    code = r.sub("^(\s*)\r\n", "", code)
    code = r.sub("(\240|\302)", " ", code)

    return code


def login():
    # # 获取验证码图片
    url = "https://www.dotcpp.com/oj/loginpage.php"
    bs.get(url)
    sleep()

    # sleep()  # 找到账号框并输入账号 H1810317091 20202020a
    bs.find_element_by_name('user_id').send_keys("H1810317091")
    # sleep()  # 找到密码框并输入密码 dotpork2020 2020porka
    bs.find_element_by_name('password').send_keys("dotpork2020")
    # sleep()  # 找到验证码框并输入验证码
    captcha = input("请输入验证码")
    bs.find_element_by_name('vcode').send_keys(captcha)
    sleep()  # 找到登陆按钮并点击
    bs.find_element_by_id('tijiao').click()


def pushCode(str, code):
    url = "https://www.dotcpp.com/oj/problem"+str+".html"
    bs.get(url)
    sleep()

    # 更改默认语言
    try:
        s1 = Select(bs.find_element_by_id("lang_chose"))
        s1.select_by_index(1)
    except:
        return False

    # sleep()

    # 找到text标签
    text = bs.find_element_by_xpath(
        "//div[@class='content_box']//div[@id='editor']//textarea")
    # 全选并清空文本
    text.send_keys(Keys.CONTROL, 'a')
    text.send_keys(Keys.BACK_SPACE)
    sleep()
    # 输入内容
    text.send_keys(code)
    # for line in code.split("\n"):
    #     text.send_keys(line)
    #     text.send_keys(Keys.ENTER)
    # sleep()

    text.send_keys(Keys.SPACE, Keys.SPACE, Keys.SPACE, Keys.SPACE,  Keys.SHIFT, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                   Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN)
    text.send_keys(Keys.BACK_SPACE)
    sleep()
    # 点击提交
    button = bs.find_element_by_xpath(
        "//form[@action='submit.php']//button[@type='button']")
    # a = input("键入以继续")
    # a = input("----------------------------\n")

    button.click()


able = [1021, 1024, 1026, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1038, 1040, 1041, 1043, 1044, 1046, 1048, 1049,
        1050, 1051, 1055, 1057, 1059, 1063, 1066, 1068, 1070, 1073, 1075, 1076, 1080, 1084, 1085, 1087, 1091, 1092, 1093, 1095,
        1096, 1097, 1099, 1100, 1103, 1106, 1107, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1117, 1118, 1119, 1123, 1128, 1129,
        1130, 1131, 1133, 1134, 1135, 1138, 1144, 1147, 1148, 1149, 1150, 1151, 1155, 1157, 1159, 1160, 1161, 1164, 1169, 1171,
        1172, 1173, 1180, 1184, 1187, 1188, 1193, 1196, 1198, 1204, 1205, 1206, 1207, 1209, 1211, 1214, 1216, 1218, 1220, 1221,
        1222, 1226, 1228, 1230, 1232, 1235, 1237, 1238, 1239, 1240, 1241, 1242, 1245, 1247, 1248, 1252, 1253, 1258, 1260, 1262,
        1265, 1266, 1267, 1269, 1274, 1278, 1280, 1285, 1287, 1289, 1291, 1292, 1294, 1296, 1297, 1300, 1302, 1304, 1305, 1311,
        1312, 1313, 1315, 1316, 1322, 1324, 1325, 1326, 1327, 1329, 1331, 1334, 1336, 1337, 1340, 1341, 1342, 1343, 1347, 1348,
        1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1361, 1378, 1382, 1386, 1388, 1390, 1391, 1392, 1395, 1397, 1399, 1400,
        1401, 1406, 1408, 1409, 1410, 1411, 1412, 1414, 1415, 1416, 1418, 1419, 1423, 1424, 1425, 1431, 1434, 1436, 1437, 1438,
        1440, 1442, 1445, 1452, 1453, 1458, 1460, 1461, 1462, 1463, 1465, 1466, 1468, 1470, 1471, 1472, 1473, 1477, 1484, 1490,
        1492, 1498, 1501, 1502, 1505, 1507, 1511, 1513, 1514, 1517, 1518, 1526, 1530, 1534, 1536, 1538, 1541, 1542, 1545, 1546,
        1547, 1549, 1550, 1551, 1553, 1554, 1555, 1557, 1561, 1562, 1563, 1565, 1566, 1567, 1568, 1569, 1572, 1575, 1578, 1580,
        1581, 1583, 1584, 1585, 1586, 1592, 1593, 1594, 1598, 1600, 1601, 1605, 1607, 1610, 1615, 1619, 1621, 1622, 1623, 1624,
        1627, 1631, 1632, 1633, 1634, 1635, 1636, 1637, 1642, 1644, 1646, 1648, 1649, 1650, 1652, 1655, 1660, 1661, 1664, 1665,
        1669, 1671, 1675, 1678, 1680, 1684, 1686, 1687, 1688, 1693, 1697, 1702, 1703, 1709, 1711, 1715, 1716, 1721, 1731, 1742,
        1747, 1751, 1754, 1755, 1756, 1757, 1758, 1759, 1772, 1774, 1775, 1776, 1790, 1793, 1797, 1798, 1799, 1800, 1801, 1805,
        1806, 1807, 1810, 1811, 1812, 1814, 1818, 1821, 1824, 1828, 1831, 1833, 1847, 1849, 1852, 1853, 1854, 1858, 1864, 1879,
        1880, 1885, 1892, 1897, 1900, 1903, 1904, 1907, 1908, 1911, 1912, 1920, 1924, 1925, 1926, 1931, 1933, 1934, 1951, 1952,
        1953, 1955, 1970, 1971, 1973, 1978, 1979, 1980, 1982, 1986, 1993, 1994, 1996, 1999, 2000, 2002, 2003, 2005, 2006, 2007,
        2033, 2043, 2053, 2057, 2075, 2081, 2083, 2088, 2091, 2102, 2112, 2114, 2121, 2131, 2132, 2138, 2161, 2181, 2187, 2198,
        2207, 2214, 2217, 2218, 2221, 2227, 2234, 2236, 2241, 2254, 2260, 2263, 2270, 2281, 2288, 2301, 2304, 2305, 2307, 2318,
        2326, 2327, 2329]

cnt = 0

bs = webdriver.Chrome()
login()
for k in range(0,401):
    i = able[k]
    url = getTitle(str(i))
    code = getCode(url)
    if code != False:
        print("####################################")
        print("https://www.dotcpp.com/oj/problem"+str(i)+".html")
        # print(code)
        print(i)
        pushCode(str(i), code)
    cnt = cnt+1
    if cnt >= 23:
        break
