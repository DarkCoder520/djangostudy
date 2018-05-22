import re
import json
import random
import requests
import time, hashlib
from taobaosplash.settings import USER_AGENTS
from urllib.parse import urlencode

def taobaodata_json(content,size_dict,color_dict,rate):
        total_product = {}
        try:
            if not rate:
                return total_product
            #match = re.findall(r'.*skuMap.*?(\{[\s\S]*?\}\})[\s\S]*', content)  #该正则效率极低
            #sibUrl_list = re.findall(r'.*sibUrl.*?\'([\s\S]*?)\'.*', content)   #该正则效率极低
            skumap_pos = content.find("skuMap")
            pattern = re.compile(r'skuMap.*?(\{[\s\S]*?\}\})[\s\S]*')
            sku_match = pattern.search(content, skumap_pos)
            if not sku_match:
                return total_product

            sibUrl_pos = content.find("sibUrl")
            pattern = re.compile(r'sibUrl.*?\'([\s\S]*?)\'.*')
            siburl_match = pattern.search(content, sibUrl_pos)
            if not siburl_match:
                return total_product

            stockStr = get_kucun(siburl_match.group(1))
            if not stockStr:
                return total_product

            stockslist = re.findall(r'[\s\S*]onSibRequestSuccess\((.*)\)\;',stockStr)
            if not stockslist:
                return total_product
            stockjson = json.loads(stockslist[0])
            skudict = stockjson['data']['dynStock']['sku']
            taobao_json_str = sku_match.group(1)
            taobaojson = json.loads(taobao_json_str)
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
                    newjson['true_price'] = round(float(market_price) * rate,1)
                    newjson['stock'] = skudict[name]['stock']
                    newjson['market_price'] = market_price
                    newjson['option'] = option
                    total_product[item['skuId']] = newjson
            return total_product
        except Exception as e:
            print(e)
            return total_product


def tianmaodata_json(content,rate):
        #使用这种方式效率不高
        #match = re.findall(r'.*TShop.Setup\(([\s\S]*?)\)[\s\S]*', str)
        total_product = {}
        try:
            if not rate:
                return total_product
            pos = content.find("TShop.Setup")
            pattern = re.compile(r'TShop\.Setup\(([\s\S]*?)\)[\s\S]*')
            match = pattern.search(content, pos)
            if not match:
                return total_product
            tianmao_json_str = match.group(1)
            tianmaojsonobj = json.loads(tianmao_json_str)
            tianmaojson_skuMap = tianmaojsonobj['valItemInfo']['skuMap']
            tianmaojson_skuList = tianmaojsonobj['valItemInfo']['skuList']
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
                newjson['true_price'] = round(float(market_price)*rate,1)
                newjson['stock'] = item['stock']
                newjson['market_price'] = market_price
                newjson['option'] = option
                total_product[item['skuId']] = newjson
            return total_product
        except Exception as e:
            print(e)
            return total_product


def get_kucun(url):
        param_list = re.findall(".*itemId=(\d+).*sellerId=(\d+).*modules=(.*)", url)
        param = {
            'itemId': param_list[0][0],
            'sellerId': param_list[0][1],
            'modules': param_list[0][2],
            'callback': 'onSibRequestSuccess'
        }
        newurl = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?"+urlencode(param)
        user_agent = random.choice(USER_AGENTS)
        '''
         动态代理使用方式：
          proxyHost = "http-cla.abuyun.com"
        proxyPort = "9030"
        # 代理隧道验证信息
        proxyUser = "HR9275380602F5OC"
        proxyPass = "6E5FA48692A67658"
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "user": proxyUser,
            "pass": proxyPass,
            "host": proxyHost,
            "port": proxyPort,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        '''
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
            'User-Agent': user_agent,
            'referer': 'https://item.taobao.com/item.htm?id='+param_list[0][0],
            "Proxy-Authorization": auth
        }
        #"Proxy-Authorization": auth
        #proxies=proxy, verify=False,allow_redirects=False
        html = ""
        while html == "":
            try:
                response = requests.get(newurl, headers=headers,proxies=proxy, verify=False,allow_redirects=False,timeout=3)
                html = response.text
                return html
            except Exception as e:
                print(e)
                time.sleep(0.5)




if __name__ == "__main__":
    taobaodata_json()
    pass