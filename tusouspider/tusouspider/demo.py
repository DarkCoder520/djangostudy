# -*- coding:utf-8 -*-

import requests
import time

spiderId = "699dfab3b9f9486b8c8e1f3ec19bf582"
secret = "c82479406ffd4c1793c28b2d19ea378c"


def gen_token():
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
    pass

"""
申请拨号服务器
"""
p = {"count": 20}
apply_headers = gen_token(spiderId, secret, p)

try:
    r = requests.get("http://api.xdaili.cn/xdaili-api/spider/applyChannels",
                     headers=apply_headers, json=p, timeout=120)
except Exception as err_info:
    r = None
    print(err_info)

if r is not None:
    print(r.status_code)
    if r.status_code == 200:
        print(r.content)
        print(r.json())
        result = r.json()
        if result["ERRORCODE"] == "0" and result["RESULT"]:
            for one in result["RESULT"]:
                print(one)
                print(one["proxyId"])
                print(one["orderno"])


"""
动态拨号
"""
dial_headers = gen_token(spiderId, secret)
url = "http://api.xdaili.cn/xdaili-api/privateProxy/getDynamicIP" + \
      "/" + one["orderno"] + "/" + one["proxyId"]
try:
    r = requests.get(url, headers=dial_headers, timeout=120)
except Exception as err_info:
    r = None
    print(err_info)

if r is not None:
    print(r.status_code)
    if r.status_code == 200:
        print(r.content)
        print(r.json())
        result = r.json()
        if result["ERRORCODE"] == "0" and result["RESULT"]:
            print(result["RESULT"]["wanIp"])
            print(result["RESULT"]["proxyport"])
