# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random,time,hashlib
from scrapy.exceptions import IgnoreRequest
from .settings import USER_AGENTS
from .settings import redis_db


redis_findlaw_dict = "findlawurl"


class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)



class RandomProxy(object):
    def process_request(self, request, spider):
        if spider.name=="findlawspider":
            orderno = "ZF20184247995dIkqrh"
            secret = "c82479406ffd4c1793c28b2d19ea378c"
            ip = "forward.xdaili.cn"
            port = "80"
            ip_port = ip + ":" + port
            timestamp = str(int(time.time()))  # 计算时间戳
            string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
            md5_string = hashlib.md5(string.encode("utf-8")).hexdigest()  # 计算sign
            sign = md5_string.upper()  # 转换成大写
            auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
            # proxy = {"http": , "https": "https://" + ip_port}
            request.meta['proxy'] = "http://" + ip_port
            request.headers['Proxy-Authorization'] = auth

    def process_response(self,request,response,spider):
        if response.status !=200:
            return request

        hl = hashlib.md5()
        hl.update(request.url.encode(encoding='utf-8'))
        md5 = hl.hexdigest()
        if redis_db.sismember(redis_findlaw_dict, md5):
            raise IgnoreRequest("Duplicate url found:%s" % request.url)
        else:
            redis_db.sadd(redis_findlaw_dict, md5)
            return response



