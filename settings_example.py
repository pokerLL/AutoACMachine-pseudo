import os

#  整体配置
sep = os.sep
BASE_DIR = os.path.dirname(__file__)
LOG_DIR = BASE_DIR + sep + 'log'

# 日志文件路径
wrong_url_log = LOG_DIR + sep + "wrong_url.txt"

# 爬虫模块参数
NEED_RANDOM_PROXY = False
NEED_RANDOM_HEADER = True
INGORE_CODE_TYPE = True
INGORE_HAVE_PASSED = False

# 代理池模块参数
API_UPDATING = False
WEB_API_URL = "http://127.0.0.1:5000/random"

# 邮件模块参数
EMAIL_HOST = 'smtp.xxx.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxx'
EMAIL_HOST_PASSWORD = 'xxx'
