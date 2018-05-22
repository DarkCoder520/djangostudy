# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import hashlib
import time
import requests
import base64
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest
from .settings import USER_AGENTS,redis_db

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


redis_tusou_dict="skwurl"
# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"
# 代理隧道验证信息
proxyUser = "H1471M7D1Y24X5GD"
proxyPass = "D9F4587769789C2F"

class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)
        request.headers.setdefault("x-requested-with", "XMLHttpRequest")


class RandomProxy(object):
    def process_request(self, request, spider):
        proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


    def process_response(self,request,response,spider):
        if response.status != 200:
            return request
        hl = hashlib.md5()
        hl.update(request.url.encode(encoding='utf-8'))
        md5 = hl.hexdigest()
        if redis_db.sismember(redis_tusou_dict, md5):
            raise IgnoreRequest("Duplicate url found:%s" % request.url)
        else:
            redis_db.sadd(redis_tusou_dict, md5)
            return response



class CustomDownloadMiddleware(object):
    def __init__(self):
        self.orderno = "ZF20184247995dIkqrh"
        self.secret = "c82479406ffd4c1793c28b2d19ea378c"
        self.ip = "forward.xdaili.cn"
        self.port = "80"
        self.ip_port = self.ip + ":" + self.port
        self.session = requests.session()


    def process_request(self, request, spider):
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        md5_string = hashlib.md5(string.encode("utf-8")).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        proxy = {"http": "http://" + self.ip_port, "https": "https://" + self.ip_port}
        headers = {"Proxy-Authorization": auth}
        response = self.session.get(request.url, headers=headers, proxies=proxy, verify=False,allow_redirects=False,timeout=20)
        if response.status_code == 200:
            return HtmlResponse(request.url, body=response.content, headers=headers, request=request)
        else:
            return request