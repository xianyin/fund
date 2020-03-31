import smtplib
from email.mime.text import MIMEText
from email.header import Header
from Logger import logger
import requests
import json
import configparser
import pymysql
import os

config_dir = os.path.split(os.path.realpath(__file__))[0]
config_path = os.path.join(config_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

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

def get_all_db_data(sql) :
    try :
        db = pymysql.connect(host = config.get('db', 'host'), port = 3306, user = config.get('db', 'user_name'),
        password = config.get('db', 'user_password'), database = config.get('db', 'database'), charset = 'utf8')
        cur = db.cursor()  # 获取会话指针，用来调用SQL语句
        # sql = 'SELECT * FROM fund_sell_history'  # 编写SQL语句
        cur.execute(sql)  # 执行SQL语句
        data = cur.fetchall()  # 提取所有数据，并赋值给data变量
        # 数据无法按照row['code']取值
        # for row in data :
        #     code = row[2]
        #     print(code)
        # print(data)
        cur.close()  # 关闭会话指针
        db.close()  # 关闭数据库链接
        return data
    except Exception :
        logger.error("Error: 数据库数据获取失败，{}".format(Exception))

def get_sell_history_data() : 
    try :
        db = pymysql.connect(host = config.get('db', 'host'), port = 3306, user = config.get('db', 'user_name'),
        password = config.get('db', 'user_password'), database = config.get('db', 'database'), charset = 'utf8')
        cur = db.cursor()  # 获取会话指针，用来调用SQL语句
        sql = 'SELECT * FROM fund_sell_history'  # 编写SQL语句
        cur.execute(sql)  # 执行SQL语句
        data = cur.fetchall()  # 提取所有数据，并赋值给data变量
        # 数据无法按照row['code']取值
        # for row in data :
        #     code = row[2]
        #     print(code)
        # print(data)
        cur.close()  # 关闭会话指针
        db.close()  # 关闭数据库链接
        return data
    except Exception :
        logger.error("Error: 数据库数据获取失败，{}".format(Exception))
    
    
# print(get_sell_history_data())
