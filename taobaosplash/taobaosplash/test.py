import json
import requests
import random
from taobaosplash.settings import USER_AGENTS
from taobaosplash.settings import COOKIE_LISTS
from urllib.parse import  urlencode
def taobaodata_json():
    with open("test2.txt", 'r', encoding="utf-8") as f:
        str = f.read()
        total_product = {}
        match = re.findall(r'.*skuMap.*?(\{[\s\S]*?\}\})[\s\S]*', str)
        sibUrl_list = re.findall(r'.*sibUrl.*?\'([\s\S]*?)\'.*', str)
        content = get_kucun(sibUrl_list[0])
        content = re.findall(r'[\s\S*]onSibRequestSuccess\((.*)\)\;',content)
        if not content:
            return total_product
        stockjson = json.loads(content[0])
        skudict = stockjson['data']['dynStock']['sku']
        size_dict = {"20509:28383": "均码"}
        color_dict = {"1627207:28320":"白色","1627207:28323":"粉色","1627207:28329":"紫色","1627207:3343219":"墨绿"}
        taobao_json_str = match[0]
        taobaojson = json.loads(taobao_json_str)
        rate = 0.5
        for name,item in taobaojson.items():
            if name in skudict.keys():
                newjson = {}
                option = {}
                namelist = name.split(";")
                size_id = namelist[1]
                color_id = namelist[2]
                if size_dict:
                    option['size'] = size_dict[size_id]
                if color_dict:
                    option['color'] = color_dict[color_id]
                market_price = item['price']
                newjson['true_price'] = float(market_price) * rate
                newjson['stock'] = skudict[name]['stock']
                newjson['market_price'] = market_price
                newjson['option'] = option
                total_product[item['skuId']] = newjson
        print(total_product)
        pass


def tianmaodata_json():
    with open("test.txt", 'r', encoding="utf-8") as f:
        str = f.read()
        #使用这种方式效率不高
        #match = re.findall(r'.*TShop.Setup\(([\s\S]*?)\)[\s\S]*', str)
        total_product = {}
        pos = str.find("TShop.Setup")
        pattern = re.compile(r'TShop\.Setup\(([\s\S]*?)\)[\s\S]*')
        match = pattern.search(str, pos)
        if not match:
            return total_product
        tianmao_json_str = match.group(1)
        tianmaojsonobj = json.loads(tianmao_json_str)
        tianmaojson_skuMap = tianmaojsonobj['valItemInfo']['skuMap']
        tianmaojson_skuList = tianmaojsonobj['valItemInfo']['skuList']
        rate = 0.25
        for name, item in tianmaojson_skuMap.items():
            newjson = {}
            option = {}
            for tianmao in tianmaojson_skuList:
                if item['skuId'] == tianmao['skuId']:
                    namestr = tianmao['names']
                    result = namestr.split(" ")
                    if len(result)>1:
                        option['size'] = namestr.split(" ")[0].strip()
                        option['color'] = namestr.split(" ")[1].strip()
                    else:
                        option['color'] = namestr.strip()
            market_price = item['price']
            newjson['true_price'] = float(market_price)*rate
            newjson['stock'] = item['stock']
            newjson['market_price'] = market_price
            newjson['option'] = option
            total_product[item['skuId']] = newjson
        print(total_product)
        pass
import re

def get_tianmaostr_by_re():
    with open("test.txt",'r',encoding="utf-8") as f:
        str = f.read()
        match = re.findall(r'.*TShop.Setup\(([\s\S]*?)\)\;.*',str)
        print(match[0])
    pass

def get_taobaostr_by_re():
    with open("test2.txt",'r',encoding="utf-8") as f:
        str = f.read()
        #match = re.findall(r'.*skuMap.*?(\{[\s\S]*?\}\})[\s\S]*propertyMemoMap:.*(\{[\s\S]*?\})[\s\S]*',str)
        #match = re.findall(r'.*skuMap.*?(\{[\s\S]*?\}\})[\s\S]*',str)
        pos = str.find("skuMap")
        pattern = re.compile(r'skuMap.*?(\{[\s\S]*?\}\})[\s\S]*')
        match = pattern.search(str, pos)
        if not match:
            return []
        skumapstr = match.group(1)

        pos = str.find("sibUrl")
        pattern = re.compile(r'sibUrl.*?\'([\s\S]*?)\'.*')
        match = pattern.search(str, pos)
        if not match:
            return []
        sibUrl = match.group(1)
        pass
        #sibUrl_list = re.findall(r'.*sibUrl.*?\'([\s\S]*?)\'.*',str)
        #content = get_kucun(sibUrl_list[0])
        #print(match[0][0])
        #print(match[0][1])
    pass

def get_kucun(url):
    #url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=560394603712&sellerId=11186712&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess"
    #url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=560394603712"
    try:
        newurl = "https:"+url+"&callback=onSibRequestSuccess"
        itemIdlist = re.findall(".*itemId=(\d+).*",url)
        user_agent = random.choice(USER_AGENTS)
        headers={
           'User-Agent':user_agent,
           'referer':'https://item.taobao.com/item.htm?id='+itemIdlist[0]
        }
        response = requests.get(newurl,headers=headers)
        return response.text
    except Exception as e:
        print(e)
    pass

class transCookie(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')  # 记得去除空格
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


def to_python_zip(text):
    items = text.split('\n')
    head_zip = {}

    for item in items:
        if 'Cookie' in item:
            item = item.replace('Cookie:', '')
            head_zip['Cookie'] = item
        elif item.startswith(":"):
            item = item.replace(':', '', 1)
            key = item.split(':')
            head_zip[':' + key[0]] = key[1]
        else:
            key = item.split(':')
            head_zip[key[0]] = key[1]
    print(head_zip)

def test():
    import time,hashlib
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
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Proxy-Authorization": auth,
        "referer":"https://item.taobao.com/item.htm?id=560863973852"
    }
    url = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm'
    param = {
                'itemId': '555794448322',
                'sellerId' :'134201161',
                'modules': 'modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract',
                'callback': 'onSibRequestSuccess'
    }
    newurl = url+"?"+urlencode(param)
    #print(newurl+"=============")
    #newurl="https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=555794448322&amp;sellerId=134201161&amp;modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess"
    r =requests.get(newurl,headers=headers,proxies=proxy,verify=False,allow_redirects=False)
    # print(r.status_code)
    # print(r.content)
    # print(r.status_code)
    # if r.status_code == 302 or r.status_code == 301:
    #     loc = r.headers['Location']
    #     url_f = "https://www.tianyancha.com" + loc
    #     print(loc)
    #     r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    #     print(r.status_code)
    #     print(r.text)
    print(r.content)


def test2():
    str = "//detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=558884522909&amp;sellerId=1595527798&amp;modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract"
    lists = re.findall(".*itemId=(\d+).*sellerId=(\d+).*modules=(.*)",str)
    print(lists)
    pass
if __name__ == "__main__":
    #taobaodata_json()
    #get_taobaostr_by_re()
    tianmaodata_json()
    pass