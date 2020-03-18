import smtplib
from email.mime.text import MIMEText
from email.header import Header
from Logger import logger
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def send_email(content, _subtype='plain', _subject="基金当前净值"):
    # 第三方 SMTP 服务
    mail_host = config.get('mail', 'mail_host')  # 设置服务器
    mail_user = config.get('mail', 'mail_user')  # 用户名
    mail_pass = config.get('mail', 'mail_pass')  # 口令
    mail_to = eval(config.get('mail', 'mail_to'))

    message = MIMEText(content, _subtype, 'utf-8')
    message['From'] = Header(mail_user)
    message['To'] = Header(",".join(mail_to))
    message['Subject'] = Header(_subject)
    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.ehlo()
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, mail_to, message.as_string())
        server.close()
        logger.info("邮件发送成功")
        return True
    except smtplib.SMTPException as err:
        logger.error("Error: 邮件发送失败,{}".format(err))
        return False

def send_dingding(content) :
    #推送钉钉服务
    headers = {"content-type":"application/json"}
    link = config.get('push', 'dingding')
    data = {
        "msgtype": "text", 
        "text": {
            "content": "消息：\n" + content
        }
    }
    r = requests.post(link, headers = headers, data = json.dumps(data))
    logger.info("钉钉发送状态：" + r.text)
    return r.text
