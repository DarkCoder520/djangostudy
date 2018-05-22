# -*- coding: utf-8 -*-
import scrapy
import random
import json
import time
import requests
import re

from urllib.parse import urlencode
from openlawspider.settings import USER_AGENTS
from openlawspider.cookieutils import TransCookie
from openlawspider.duplicateutils import drop_duplicate_url
from openlawspider.items import OpenlawspiderItem



class WenshuspiderSpider(scrapy.Spider):
    name = 'wenshuspider'
    allowed_domains = ['openlaw.cn']
    start_urls = ['http://openlaw.cn/search/judgement/default']
    #city_list = ['西安市','咸阳市','汉中市','宝鸡市','渭南市','榆林市','安康市','延安市','商洛市','铜川市']
    #judgeResult_list= ['Defeat','Unknow','Victory','Half','Other','Revoke']


    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "host": "openlaw.cn"
        }
        self.params = {
            "docType": "Verdict",
            "causeId": "a3ea79cf193f4e07a27a900e29585dbb",
            "judgeDateYear": "2015",
            "zone": "陕西省",
            "keyword": "离婚纠纷",
        }

    def send_jToken_request(self,**kwargs):
        cookie_list = [str(x, encoding="utf-8").split(";")[0] for x in kwargs['cookies']]
        cmp = re.compile('window.v="(.*)";')
        rst = cmp.findall(kwargs['content'])
        if len(rst):
            v_token = rst[0]
            j_token = v_token[2:4] + 'n' + v_token[0:1] + 'p' + v_token[4:8] + 'e' + v_token[1:2] + v_token[len(v_token) - 17:] + v_token[8:16]
            cookiestr = "j_token=" + j_token
            cookie_list.append(cookiestr)
            user_agent = random.choice(USER_AGENTS)
            headers = self.headers.copy()
            headers['User-Agent'] = user_agent
            headers['Cookie'] = ";".join(cookie_list)
            return scrapy.Request(kwargs['url'], headers=headers,callback=eval(kwargs['callback']),dont_filter=True)


    def start_requests(self):
        user_agent = random.choice(USER_AGENTS)
        #headers = self.headers.copy()
        #headers['User-Agent'] = user_agent
        metas={"callbackfuc":"self.parse_result"}
        for url in self.start_urls:
            url = url + "?" + urlencode(self.params)
            yield scrapy.Request(url,meta=metas,dont_filter=True)


    def parse(self, response):
        callbackfuc = response.meta.get("callbackfuc","")
        cookies = response.headers.getlist('Set-Cookie')
        url = response.url
        content = response.text
        yield self.send_jToken_request(url=url,cookies=cookies,content=content,callback=callbackfuc)


    def parse_result(self, response):
        judgeresults = response.xpath('//section[@id="group-judgeresult"]/ul/li/a')
        params = self.params.copy()
        headers = self.headers.copy()
        metas = {"callbackfuc": "self.parse_wenshu_link"}
        for judgeresult in judgeresults:
            user_agent = random.choice(USER_AGENTS)
            headers['User-Agent'] = user_agent
            data_judgeresult = judgeresult.xpath("./@data-judgeresult").extract_first("")
            judgeresultstr = judgeresult.xpath("./text()").extract_first("")
            judgeCount = re.sub("\D","",judgeresultstr)
            if data_judgeresult and judgeresultstr:
                if int(judgeCount)<2000:
                    params['judgeResult'] = data_judgeresult.strip()
                    url = self.start_urls[0] + "?" + urlencode(params)
                    yield scrapy.Request(url,meta=metas,headers=headers, callback=self.parse)
                else:
                    city_list = response.xpath('//section[@id="group-zone"]/ul/li/a/text()').extract()
                    for citystr in city_list:
                        index = citystr.find("（")
                        city = citystr[:index]
                        city_case_count = re.sub("\D","",citystr)
                        if int(city_case_count) > 2000:
                            courtid_list = response.xpath('//section[@id="group-court"]/ul/li/a/@data-courtid').extract()
                            #for courtId in courtid_list:
                            params['courtId'] = courtid_list[0]
                            url = self.start_urls[0] + "?" + urlencode(params)
                            yield scrapy.Request(url,meta=metas,headers=headers, callback=self.parse)
                        else:
                            params['zone'] = city
                            url = self.start_urls[0] + "?" + urlencode(params)
                            yield scrapy.Request(url,meta=metas,headers=headers, callback=self.parse)


    def parse_wenshu_link(self,response):
        next_page = response.xpath('//ul[@class="page-numbers"]/li/a[@class="next page-numbers"]/@href').extract_first("")
        articles = response.xpath('//main[@id="content"]/div/article/h3/a')
        metas={"callbackfuc":"self.parse_wenshu_content"}
        #for article in articles:
        article=articles[0]
        title = article.xpath("string(.)").extract_first("")
        link = article.xpath("./@href").extract_first("")
        if title and link:
            url = "http://openlaw.cn"+link
            is_duplicate = drop_duplicate_url(url)
            if not is_duplicate:
                yield scrapy.Request(url=url,meta=metas,callback=self.parse)

        # if next_page:
        #     metas = {"callbackfuc": "self.parse_wenshu_link"}
        #     url = "http://openlaw.cn/search/judgement/default" + next_page
        #     yield scrapy.Request(url=url,meta=metas,callback=self.parse)


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