import requests
import json
import time
import hashlib
import random
from urllib.parse import urlencode
from lxml import etree
USER_AGENTS=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Win64; x64; Trident/4.0)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        ]

def baidu():
    orderno = "ZF20184247995dIkqrh"
    secret = "c672faf1c26c4289a997b7c1911a9bb8"
    ip = "forward.xdaili.cn"
    port = "80"
    ip_port = ip + ":" + port
    timestamp = str(int(time.time()))  # 计算时间戳
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
    md5_string = hashlib.md5(string.encode("utf-8")).hexdigest()  # 计算sign
    sign = md5_string.upper()  # 转换成大写
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    user_agent = random.choice(USER_AGENTS)
    headers = {
        "Cookie":"BIDUPSID=6786723251008418C0CE3A3B7F366399; PSTM=1521772312; BAIDUID=ADB50FF729F8F9B78CB9FB2FE22D669B:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=mxaM2RSRXVxYXNSVlEwSFdELTZBcWk4djZ5V2pULXB3R0FDc0VPNlp4NVB0d2RiQVFBQUFBJCQAAAAAAAAAAAEAAABZGo1Bsfm78MG91tjM7HR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE8q4FpPKuBaM; PSINO=6; BDRCVFR[YDNdHN8k-cs]=9xWipS8B-FspA7EnHc1QhPEUf; BDRCVFR[PaHiFN6tims]=9xWipS8B-FspA7EnHc1QhPEUf; BAIDU_SSP_lcr=https://zhidao.baidu.com/list; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1524623503,1524647372,1524651804,1524706354; H_PS_PSSID=1429_21111_20927; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1524706783",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }
    params = {
        "cid": "103102",
        "type": "hot",
        "ie": "utf8",
        "rn": "30",
        "pn": "60",
        "_pjax": "#j-question-list-pjax-container"
    }
    response = requests.get("https://zhidao.baidu.com/list?"+urlencode(params),headers=headers,timeout=300)
    html = etree.HTML(response.content.decode("gbk"))
    question_list = html.xpath('//li[@class="question-list-item"]/div/div[@class="question-title"]/a/text()')
    print(response.content.decode("gbk"))
    # timestamp = int(time.time())
    # first_url = "https://zhidao.baidu.com/task/api/getmytasklist?popFlag=1&status=done&_="+str(timestamp)
    # first_response = requests.get(first_url,headers)
    # first_json = json.loads(first_response.text)
    # if first_json['errmsg'] =="success!":
    #     response = requests.get("https://zhidao.baidu.com/list?cid=103102&type=hot&rn=30&pn=0&ie=utf8&_pjax=%23j-question-list-pjax-container",headers=headers)
    #     print(response.content)
    #     pass


if __name__ == "__main__":
    baidu()