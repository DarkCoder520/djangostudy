# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
import hashlib
import requests
import re
from .settings import USER_AGENTS
from lxml import html
from scrapy.http import HtmlResponse


class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)


class RandomProxy(object):
    def process_request(self, request, spider):
        orderno = "ZF20185360445J74FS"
        secret = "6fa047ec933441f4b3b24fec527d2e72"
        ip = "forward.xdaili.cn"
        port = "80"
        ip_port = ip + ":" + port
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        md5_string = hashlib.md5(string.encode("utf-8")).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        proxies = {"http": ip, "https": "https://" + ip_port}
        #request.meta['proxy'] = "http://" + ip_port
        #headers={'User-Agent':random.choice(USER_AGENTS),'Proxy-Authorization':auth}
        headers = request.headers.copy()
        headers['Proxy-Authorization'] = auth
        ret_origin = requests.get(request.url, headers=headers,proxies=proxies)
        #print(ret_origin.text)
        cookies = requests.utils.dict_from_cookiejar(ret_origin.cookies)
        # 第二步，js代码并还原j_token计算过程，正则匹配window.v
        cmp = re.compile('window.v="(.*)";')
        rst = cmp.findall(ret_origin.text)
        if len(rst):
            v_token = rst[0]
            j_token = v_token[2:4] + 'n' + v_token[0:1] + 'p' + v_token[4:8] + 'e' + v_token[1:2] + v_token[len(
                v_token) - 17:] + v_token[8:16]
            cookies['j_token'] = j_token
            ret_next = requests.get(request.url, headers=headers, cookies=cookies)
            return HtmlResponse(url=request.url,body=ret_next.text,headers=headers,request=request)
        return request


class CustomDownloadMiddleware(object):
    def __init__(self):
        self.orderno = "ZF20184247995dIkqrh"
        self.secret = "6fa047ec933441f4b3b24fec527d2e72"
        self.ip = "forward.xdaili.cn"
        self.port = "80"
        self.ip_port = self.ip + ":" + self.port
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "host": "openlaw.cn",
        }

    def process_request(self, request, spider):
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        md5_string = hashlib.md5(string.encode("utf-8")).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        proxies = {"http": self.ip, "https": "https://" + self.ip_port}
        user_agent = random.choice(USER_AGENTS)
        self.headers['Proxy-Authorization'] = auth
        self.headers['User-Agent'] = user_agent
        ret_origin = requests.get(request.url, headers=self.headers, proxies=proxies)
        cookies = requests.utils.dict_from_cookiejar(ret_origin.cookies)
        cmp = re.compile('window.v="(.*)";')
        rst = cmp.findall(ret_origin.text)
        if len(rst):
            v_token = rst[0]
            j_token = v_token[2:4] + 'n' + v_token[0:1] + 'p' + v_token[4:8] + 'e' + v_token[1:2] + v_token[len(
                v_token) - 17:] + v_token[8:16]
            cookies['j_token'] = j_token
            ret_next = requests.get(request.url, headers=self.headers, cookies=cookies)
            return HtmlResponse(request.url,body=ret_next.content, headers=self.headers, request=request)
        return request

    def process_response(self, request, response, spider):
        return response



