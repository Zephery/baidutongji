### 谈谈个人网站的建立（四）—— 日志系统的建立 
建立网站少不了日志系统，用来查看网站的各种流量，其中，最常用的方法还是使用ELK，但是，本网站的服务器配置实在太低了  
 <center>
 
 ![](http://ohlrxdl4p.bkt.clouddn.com/images/4f70486620170913090343.png)
 
 </center>

压根就跑不起ELK，所以只能使用其他方式，目前最常用的有[百度统计](https://tongji.baidu.com/web/welcome/login)和[友盟](https://www.umeng.com/)，这里，本人使用的是百度统计，提供了API给开发者使用，能够将自己所需要的图表移植到自己的网站上，













百度统计python最简单版本
```python
import json
import time
import datetime
import urllib.parse
import urllib.request

base_url = "https://api.baidu.com/json/tongji/v1/ReportService/getData"


class Baidu(object):
    def __init__(self, siteId, username, password, token):
        self.siteId = siteId
        self.username = username
        self.password = password
        self.token = token

    def getresult(self, start_date, end_date, method, metrics):
        body = {"header": {"account_type": 1, "password": self.password, "token": self.token,
                           "username": self.username},
                "body": {"siteId": self.siteId, "method": method, "start_date": start_date,
                         "end_date": end_date,
                         "metrics": metrics}}
        data = bytes(json.dumps(body), 'utf8')
        req = urllib.request.Request(base_url, data)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        return the_page.decode("utf-8")


if __name__ == '__main__':
    # 日期开始
    start_date = time.strftime("%Y%m%d", time.localtime())
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    fifteenago = today - datetime.timedelta(days=7)
    print(str(yesterday).replace("-", ""), str(fifteenago).replace("-", ""))
    end, start = str(yesterday).replace("-", ""), str(fifteenago).replace("-", "")
    # 日期结束
    bd = Baidu(yousiteid, "your username", "your password", "your token")
    result = bd.getresult(start, end, "overview/getTimeTrendRpt",
                          "pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time")
    result = json.loads(result)
    base = result["body"]["data"][0]["result"]["items"]
```









