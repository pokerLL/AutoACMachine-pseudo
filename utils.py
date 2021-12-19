import itertools

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from settings import *


def send_message(msg, subject, receiver):
    sender = EMAIL_HOST_USER
    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = Header(sender)
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(EMAIL_HOST, EMAIL_PORT)  # 25 为 SMTP 端口号
        smtpObj.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
        return True
    except:
        print("邮件发送失败")
        return False


def flatten(ls):
    return list(itertools.chain.from_iterable(ls))
