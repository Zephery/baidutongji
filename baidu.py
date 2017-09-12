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
        base_url = "https://api.baidu.com/json/tongji/v1/ReportService/getData"
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
    bd = Baidu(10879516, "ZepheryWen", "wenzhihuai2017", "bad4fda9a063476f2976c24416ec02ad")
    result = bd.getresult(start, end, "overview/getTimeTrendRpt",
                          "pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time")
    result = json.loads(result)
    base = result["body"]["data"][0]["result"]["items"]
    print(base)
    date = base[0]
