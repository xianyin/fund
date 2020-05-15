import requests
import time
import json,re
import MyUtils as util

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
# fund_codes = ['519697', '110011','001704', '163210', '000363', '166002', '206009', '001178']
fund_codes = {'主动基金':['519697', '110011','001704'], 
    '九雾组合':['320022', '000363', '166002', '206009', '001178']}
    
#获取当前时间的字符串形式
def get_current_time() :
    now = int(time.time())
    time_struct = time.localtime(now)
    str_time = time.strftime('%Y-%m-%d %H:%M', time_struct)
    return str_time
print(get_current_time())

#根据code码获取基金信息字典
def get_fund_value_json(code) :
    link = 'http://fundgz.1234567.com.cn/js/' + code + '.js?rt=' + str(round(time.time()*1000))
    r = requests.get(link, headers = headers, timeout = 10)
    j_dic = json.loads(re.match(".*?({.*}).*", r.text, re.S).group(1))
    # print(r.text)
    return j_dic
#根据基金信息拼装成最终消息内容
def print_fund_value(content) :
    # fund_codes本身就是dict
    items = fund_codes.items()
    for key, value in items :
        content += key + ':\n'
        average_gszzl = 0.0
        count_gszzl = 0
        for code in value : 
            _json = get_fund_value_json(code)
            count_gszzl += 1 
            average_gszzl += (float)(_json['gszzl'])
            content += '\t<' + _json['name'] + '>估算涨跌幅为:' + _json['gszzl'] + '%. \t当前时间：' + _json['gztime'] + '\n'
        content += '组合平均涨幅：' + '%.2f%%' % (average_gszzl/count_gszzl) + '\n'
    return content    

# #获取上证指数值
# def get_fund_index() :
#     link = 'http://26.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405048480031612907_1583982715293&pn=1&pz=21&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fs=i:1.000001&fields=f1,f2,f3,f4,f14'
#     r = requests.get(link, headers = headers, timeout = 10)
#     j_dic = json.loads(re.match(".*?({.*}).*", r.text, re.S).group(1))
#     return j_dic
# def get_tiantian_dict(link) :
#     #  link = 'http://26.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405048480031612907_1583982715293&pn=1&pz=21&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fs=i:1.000001&fields=f1,f2,f3,f4,f14'
#     r = requests.get(link, headers = headers, timeout = 10)
#     j_dic = json.loads(re.match(".*?({.*}).*", r.text, re.S).group(1))
#     return j_dic

# 打印指数值
def print_fund_index(content) :
    links = ['http://26.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405048480031612907_1583982715293&pn=1&pz=21&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fs=i:1.000001&fields=f1,f2,f3,f4,f14', 'http://53.push2.eastmoney.com/api/qt/ulist.np/get?fid=f3&pi=0&pz=40&po=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&fields=f14,f12,f13,f2,f3,f4&np=1&secids=2C100.NDX%2C100.SPX', 'http://53.push2.eastmoney.com/api/qt/ulist.np/get?fid=f3&pi=0&pz=40&po=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&fields=f14,f12,f13,f2,f3,f4&np=1&secids=2C100.NDX%2C100.DJIA']
    # mail_content = content
    for link in links :
        r = requests.get(link, headers = headers, timeout = 10)
        j_dic = json.loads(re.match(".*?({.*}).*", r.text, re.S).group(1))
        fund_index_value = j_dic
        fund_index_value = fund_index_value.get('data').get('diff')
        fund_index_value = fund_index_value[0]
        fund_index_name = fund_index_value.get('f14')
        fund_index_range = str(fund_index_value.get('f3'))
        fund_index_price = str(fund_index_value.get('f2'))
        #为何必须加这一句，否则会报错呢？
        content += ''
        content += fund_index_name + '当前净值：' + fund_index_price + '，涨跌幅：' + fund_index_range + '%\n'

    return content
# 打印卖出基金当前涨跌幅
def print_sell_change(content) :
    db_data = util.get_sell_history_data()
    content += '\n'
    for row in db_data :
        fund_code = row[2]
        # 根据基金码获取基金信息
        fund_dict = get_fund_value_json(fund_code)
        percentage = (float(fund_dict['dwjz']) - float(row[3])) / float(row[3])
        # print(fund_dict['dwjz'])
        content += '<' + fund_dict['name'] + '>截止到' + fund_dict['jzrq'] + '基金涨跌幅为：' + '%.2f%%' % (percentage * 100)
        # print(content)
    return content


mail_content = ''
mail_content = print_fund_value(mail_content)
mail_content += '\n'
mail_content = print_fund_index(mail_content)
mail_contet = mail_content + '\n'
mail_content = print_sell_change(mail_content)

print(mail_content)   
# util.send_email(mail_content)
util.send_dingding(mail_content)
# print_sell_change("")

