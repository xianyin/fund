import sys
import requests
import json
import schedule
import datetime
import time
import random
import MyUtils as util

# 初始化钉钉发送开关
dingding_flag = [True, True, True, True, True]

#获取当前时间的字符串形式
def get_current_time() :
    now = int(time.time())
    time_struct = time.localtime(now)
    str_time = time.strftime('%Y-%m-%d %H:%M', time_struct)
    return str_time

# get蛋卷数据，返回json
def get_url_json(url) :
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    r = requests.get(url, headers = headers, timeout = 10)
    _json = json.loads(r.text)
    return _json

def send_dingding(count, content) :
    global dingding_flag
    if (dingding_flag[count]) :
        util.send_dingding(content)
        dingding_flag[count] = False

def check_plan() :
    sql = 'select name,plan_url,detail_url from fund_plan'
    db_data = util.get_all_db_data(sql)
    content = ''
    count = 0
    for row in db_data :
        # name = row[0]
        plan_url = row[1]
        detail_url = row[2]
        _json = get_url_json(plan_url)
        last_trade_date_fmt = _json.get('data').get('last_trade_date_fmt')
        now_date_fmt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 发车日期等于今天
        if (last_trade_date_fmt == now_date_fmt) :
            detail_json = get_url_json(detail_url)
            content = '<' + _json.get('data').get('plan_name') + '> 已发车，发车时间：' + get_current_time() +\
                '.发车方案：'
            for item in detail_json.get('data').get('items') :
                content += '<' +item.get('fd_name') + '>'
            send_dingding(count, content)        
        count += 1

# 控制定时的总任务
def job() :
    flag = True
    global dingding_flag
    print('今日任务开始，当前时间：' + get_current_time())
    while flag :
        # 当天任务只执行到15点
        if (datetime.datetime.now().hour > 14) :
            print("今日已跑完，当前时间：" + get_current_time())
            # 初始化钉钉发送开关
            dingding_flag = [True, True, True, True, True]
            flag = False
        # 真正的check方法
        check_plan()
        # 1分钟检测一次。防爬
        time.sleep(60 + random.randint(0, 15))
            

# 设置定时任务
# schedule.every().tuesday.at("00:54").do(job)

schedule.every().monday.at("09:30").do(job)
schedule.every().tuesday.at("09:30").do(job)
schedule.every().wednesday.at("09:30").do(job)
schedule.every().thursday.at("09:30").do(job)
schedule.every().friday.at("09:30").do(job)

while True :
    schedule.run_pending()
    # time.sleep(1)
