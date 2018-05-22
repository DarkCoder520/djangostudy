# -*- coding: utf-8 -*-
import scrapy
import random
import json
import time
import hashlib
import re

from urllib.parse import urlencode
from scrapy_splash import SplashRequest
from openlawspider.settings import USER_AGENTS
from openlawspider.cookieutils import TransCookie
from openlawspider.duplicateutils import drop_duplicate_url
from openlawspider.items import OpenlawspiderItem


RENDER_HTML_URL = "http://192.168.99.100:8050/execute"


class WenshuspiderSpider(scrapy.Spider):
    name = 'wenshuspider'
    allowed_domains = ['openlaw.cn']
    start_urls = ['http://openlaw.cn/search/judgement/default']
    cookie_list=[]
    script_str = '''
             function main(splash, args)
                splash:set_custom_headers({
                   ["User-Agent"] = args.user_agent,
                   ["Proxy-Authorization"] = args.auth 
                })
                splash:on_request(function(request)
                        request:set_proxy{'forward.xdaili.cn', '80', username='', password='', type='HTTPS'}
                end)
                assert(splash:go(args.url))
                assert(splash:wait(args.wait))
                return splash:html()
             end
          '''
    #city_list = ['西安市','咸阳市','汉中市','宝鸡市','渭南市','榆林市','安康市','延安市','商洛市','铜川市']
    #judgeResult_list= ['Defeat','Unknow','Victory','Half','Other','Revoke']

    def __init__(self):
        cookiestr_ty = "Hm_lvt_a105f5952beb915ade56722dc85adf05=1525421190,1525655862,1525742690,1525742715; SESSION=ZjhjOGRmNDUtZjBhMC00YWFmLTk3YTYtODMxM2FjYWRjODRi; Hm_lpvt_a105f5952beb915ade56722dc85adf05=1525854714"
        cokkiestr_cgx = "Hm_lvt_a105f5952beb915ade56722dc85adf05=1525415255,1525847286; SESSION=ZTU1MTBiZmMtZmJmZi00NTY2LThjOWEtZmUyMDZlN2YyN2Y3; Hm_lpvt_a105f5952beb915ade56722dc85adf05=1525853947"
        #cookies_ty = TransCookie(cookiestr_ty).stringToDict()
        cookies_cgx = TransCookie(cokkiestr_cgx).stringToDict()
        self.cookie_list.append(cookiestr_ty)
        self.cookie_list.append(cokkiestr_cgx)


    def send_splash_request(self,**kwargs):
        user_agent = random.choice(USER_AGENTS)
        url = kwargs['url']
        orderno = "ZF20185360445J74FS"
        secret = "6fa047ec933441f4b3b24fec527d2e72"
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        md5_string = hashlib.md5(string.encode("utf-8")).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        body = json.dumps({
            'wait': 1.5,
            'lua_source': self.script_str,
            'url': url,
            'user_agent': user_agent,
            'auth':auth
        })
        #'proxy_authorization':auth,
        headers = {'Content-Type': 'application/json', 'User-Agent': user_agent}
        return SplashRequest(RENDER_HTML_URL, method="POST", headers=headers, callback=eval(kwargs['callback']), body=body,dont_filter=True)


    def start_requests(self):
        params = {
            "docType": "Verdict",
            "causeId": "a3ea79cf193f4e07a27a900e29585dbb",
            "judgeDateYear": "2015",
            "zone": "陕西省",
            "keyword": "离婚纠纷",
        }
        for url in self.start_urls:
           url = url + "?" + urlencode(params)
           yield self.send_splash_request(url=url,callback="self.parse_result")


    def parse_result(self, response):
        judgeresults = response.xpath('//section[@id="group-judgeresult"]/ul/li/a')
        params = {
            "docType": "Verdict",
            "causeId": "a3ea79cf193f4e07a27a900e29585dbb",
            "judgeDateYear": "2015",
            "zone": "陕西省",
            "keyword": "离婚纠纷",
        }
        for judgeresult in judgeresults:
            data_judgeresult = judgeresult.xpath("./@data-judgeresult").extract_first("")
            judgeresultstr = judgeresult.xpath("./text()").extract_first("")
            judgeCount = re.sub("\D","",judgeresultstr)
            if data_judgeresult and judgeresultstr:
                if int(judgeCount)<2000:
                    params['judgeResult'] = data_judgeresult.strip()
                    url = self.start_urls[0] + "?" + urlencode(params)
                    yield self.send_splash_request(url=url,callback="self.parse_wenshu_link")
                else:
                    city_list = response.xpath('//section[@id="group-zone"]/ul/li/a/text()').extract()
                    for citystr in city_list:
                        index = citystr.find("（")
                        city = citystr[:index]
                        city_case_count = re.sub("\D","",citystr)
                        if int(city_case_count) > 2000:
                            courtid_list = response.xpath('//section[@id="group-court"]/ul/li/a/@data-courtid').extract()
                            for courtId in courtid_list:
                                params['courtId'] = courtId
                                url = self.start_urls[0] + "?" + urlencode(params)
                                yield self.send_splash_request(url=url,callback="self.parse_wenshu_link")
                        else:
                            params['zone'] = city
                            url = self.start_urls[0] + "?" + urlencode(params)
                            yield self.send_splash_request(url=url,callback="self.parse_wenshu_link")


    def parse_wenshu_link(self,response):
        next_page = response.xpath('//ul[@class="page-numbers"]/li/a[@class="next page-numbers"]/@href').extract_first("")
        articles = response.xpath('//main[@id="content"]/div/article/h3/a')
        for article in articles:
            title = article.xpath("string(.)").extract_first("")
            link = article.xpath("./@href").extract_first("")
            if title and link:
                url = "http://openlaw.cn"+link
                is_duplicate = drop_duplicate_url(url)
                if not is_duplicate:
                    yield self.send_splash_request(url=url,callback="self.parse_wenshu_content")

        if next_page:
            url = "http://openlaw.cn/search/judgement/default" + next_page
            yield self.send_splash_request(url=url,callback="self.parse_wenshu_link")


    def parse_wenshu_content(self,response):
        lawItem = OpenlawspiderItem()
        content_data_selectors = response.xpath('//main[@id="content"]/div/article/div[@id="entry-cont"]/div/div[@class="part"]')
        content_list = []
        for content_data in content_data_selectors:
            contentstr = content_data.xpath("string(.)").extract_first("")
            content_list.append(contentstr.strip())
        wenshu_content = "".join(content_list)
        title_data = response.xpath('//main[@id="content"]/div/article/header/h2')
        title = title_data.xpath("string(.)").extract_first("")
        if title and wenshu_content:
            lawItem['content'] = wenshu_content.strip()
            lawItem['title'] = title.strip()
            yield lawItem