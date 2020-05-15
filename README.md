# fund
### 功能描述
可直接运行的类：[FundClient.py](https://github.com/xianyin/fund/blob/master/FundClient.py "FundClient.py")和[DanjuanClient.py](https://github.com/xianyin/fund/blob/master/DanjuanClient.py "DanjuanClient.py")
FundClient：基金净值实时查询和预警功能。
DanjuanClient：蛋卷基金的发车提醒和组合的实时涨跌。
使用时请自行创建config.ini文件，格式如下：
```
[mail]
mail_host = 
mail_user = 
mail_pass = 
mail_to = [""]

[push]
dingding = "钉钉机器人URL"

[db]
host = 
user_name = 
user_password = 
database = 
```
####*已实现：*
1. 可自定义基金组合
2. 可输出实时的涨幅
3. 可输出实时的中证、标普、道琼斯指数
4. 支持邮件和钉钉两种消息推送方式
5. 支持记录割肉详情，并输出当前差值。
6. 蛋卷基金的发车提醒和组合的实时涨跌。

####*接下来要实现：*
1. 基金补仓计算和提醒

