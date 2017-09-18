### 谈谈个人网站的建立（四）—— 日志系统的建立 
建立网站少不了日志系统，用来查看网站的访问次数、停留时间、抓取量、目录抓取统计、页面抓取统计等，其中，最常用的方法还是使用ELK，但是，本网站的服务器配置实在太低了（1GHZ、2G内存），压根就跑不起ELK，所以只能寻求其他方式，目前最常用的有[百度统计](https://tongji.baidu.com/web/welcome/login)和[友盟](https://www.umeng.com/)，这里，本人使用的是百度统计，提供了API给开发者使用，能够将自己所需要的图表移植到自己的网站上。日志是网站及其重要的文件，通过对日志进行统计、分析、综合，就能有效地掌握网站运行状况，发现和排除错误原因，了解客户访问分布等，更好的加强系统的维护和管理。下面是我的百度统计的概览页面：
<div align="center">

![](http://ohlrxdl4p.bkt.clouddn.com/baidutongji3333.png?imageView2/2/w/300)

</div>

企业级的网站日志不能公开，但是我的是个人网站，用来跟大家一起学习的，所以，需要将百度的统计页面展示出来，但是，百度并不提供日志的图像，只提供API给开发者调用，而且还限制访问次数，一天不能超过2000次，这个对于实时统计来说，确实不够，所以只能展示前几天的访问统计。这里的日志系统分为三个步骤：1.API获取数据；2.存储数据；3.展示数据。页面效果如下：
<div align="center">

![](http://ohlrxdl4p.bkt.clouddn.com/images/20170918090524.png)

![](http://ohlrxdl4p.bkt.clouddn.com/images/20170918090534.png)

![](http://ohlrxdl4p.bkt.clouddn.com/images/20170918090546.png)

</div>

百度统计提供了Tongji API的Java和Python版本，这两个版本及其复杂，可用性极低，所以，本人用Python写了个及其简单的通用版本，整体只有28行，代码在这，[https://github.com/Zephery/baidutongji](https://github.com/Zephery/baidutongji)。下面是具体过程

## 1.网站代码安装
先在[百度统计]()中注册登录之后，进入管理页面，新增网站，然后在代码管理中获取安装代码，大部分人的代码都是类似的，除了hm.js?后面的参数，是记录该网站的唯一标识。
```java
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?e580b8db831811a4aaf4a8f3e30034dc";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
```
同时，需要在申请其他设置->数据导出服务中开通数据导出服务，百度统计Tongji API可以为网站接入者提供便捷的获取网站流量数据的通道。
![]()

## 2.根据API获取数据
[官网的API](https://tongji.baidu.com/dataapi/file/TongjiApiFile.pdf)详细的记录了接口的参数以及解释，
链接：[https://api.baidu.com/json/tongji/v1/ReportService/getData](https://api.baidu.com/json/tongji/v1/ReportService/getData),详细的官方报告请访问官网[TongjiApi](https://tongji.baidu.com/dataapi/file/TongjiApiFile.pdf "百度统计")
所需参数（必须）：

|  参数名称 | 参数类型  |描述   |
| ------------ | ------------ | ------------ |
| site_id  | uint  | 站点ID|
|method|string|要查询的报告|
|start_date|string|查询起始时间|
|end_date|string|查询结束时间|
|metrics|string|自定义指标|
其中，参数start_date和end_date的规定为：yyyyMMdd，这里我们使用python的原生库，datetime、time，获取昨天的时间以及前七天的日期。
```python
start_date = time.strftime("%Y%m%d", time.localtime())
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
fifteenago = today - datetime.timedelta(days=7)
end, start = str(yesterday).replace("-", ""), str(fifteenago).replace("-", "")
```

## 3.构建请求
说明：siteId可以根据个人百度统计的链接获取，也可以使用Tongji API的第一个接口列表获取用户的站点列表。
```python
body={
    "header": {
        "account_type": 1,
        "password": "password",
        "token": "开通统计API的token",
        "username": "用户名"
    },
    "body": {
        "siteId": "域名id",
        "method": "visit/district/a", # 地域访问
        "start_date": start,
        "end_date": end,
        "metrics": "pv_count,visitor_count,avg_visit_time" #所需要的指标
    }
}
```
## 4.对获取的数据解析
python中酷炫的语法


## 5.完整代码
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
    end, start = str(yesterday).replace("-", ""), str(fifteenago).replace("-", "")
    # 日期结束
    bd = Baidu(yoursiteid, "username", "password", "token")
    result = bd.getresult(start, end, "overview/getTimeTrendRpt",
                          "pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time")
    result = json.loads(result)
    base = result["body"]["data"][0]["result"]["items"]
    print(base)

```

## 6.展示数据
（1）PV、UV折线图
（2）地域访问量