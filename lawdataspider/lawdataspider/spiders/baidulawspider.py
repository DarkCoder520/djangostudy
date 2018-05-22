# -*- coding: utf-8 -*-
import scrapy
import random

from urllib.parse import urlencode
from lawdataspider.settings import USER_AGENTS
from lawdataspider.items import LawdataspiderItem
from lawdataspider.cookieutils import transCookie

class BaidulawspiderSpider(scrapy.Spider):
    name = 'baidulawspider'
    allowed_domains = ['zhidao.baidu.com']
    start_urls = ['https://zhidao.baidu.com/list']


    divorce_list = ["离婚"]
    jiedai_list = ["民间借贷"]
    traffic_tag_list = ["车祸", "罚单", "交通事故", "交通事故调解", "交通事故赔偿",
                        "交通事故争议", "酒驾", "逆行", "违章", "无证驾驶", "责任认定", "肇事",
                        "肇事逃逸", "撞车", "撞人"]
    cid_dict = {"103102":divorce_list,"103111":jiedai_list,"103104":traffic_tag_list}

    #https://zhidao.baidu.com/list?cid=103102&type=hot&rn=30&pn=0&ie=utf8&_pjax=%23j-question-list-pjax-container

    def start_requests(self):
        user_agent = random.choice(USER_AGENTS)
        cookiestr = "IKUT=1708; BIDUPSID=6786723251008418C0CE3A3B7F366399; PSTM=1521772312; BAIDUID=ADB50FF729F8F9B78CB9FB2FE22D669B:FG=1; BDUSS=mxaM2RSRXVxYXNSVlEwSFdELTZBcWk4djZ5V2pULXB3R0FDc0VPNlp4NVB0d2RiQVFBQUFBJCQAAAAAAAAAAAEAAABZGo1Bsfm78MG91tjM7HR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE8q4FpPKuBaM; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1525229162,1525229710; H_PS_PSSID=; PSINO=6; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1525248454"
        cookies = transCookie(cookiestr).stringToDict()
        headers = {
            "User-Agent":user_agent,
            "Host":"zhidao.baidu.com",
            "Content-Type":"application/x-www-form-urlencoded",
            "X-PJAX-Container":"#j-question-list-pjax-container",
            "X-PJAX":"true",
            "X-Requested-With":"XMLHttpRequest"
        }
        for cid,tags in self.cid_dict.items():
            for tag in tags:
                for page in range(0,26):
                    params = {
                    "tag": tag,
                    "cid": cid,
                    "ie": "utf8",
                    "rn": "30",
                    "pn": str(page*30),
                    "_pjax": "#j-question-list-pjax-container"
                }
                    for url in self.start_urls:
                        yield scrapy.Request(url+"?"+urlencode(params),headers=headers,cookies=cookies)


    def parse(self, response):
        link_list = response.xpath('//li[@class="question-list-item"]/div/div[1]/a/@href').extract()
        user_agent = random.choice(USER_AGENTS)
        cookiestr = "IKUT=1708; BIDUPSID=6786723251008418C0CE3A3B7F366399; PSTM=1521772312; BAIDUID=ADB50FF729F8F9B78CB9FB2FE22D669B:FG=1; BDUSS=mxaM2RSRXVxYXNSVlEwSFdELTZBcWk4djZ5V2pULXB3R0FDc0VPNlp4NVB0d2RiQVFBQUFBJCQAAAAAAAAAAAEAAABZGo1Bsfm78MG91tjM7HR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE8q4FpPKuBaM; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1525229162,1525229710; H_PS_PSSID=; PSINO=6; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1525248454"
        cookies = transCookie(cookiestr).stringToDict()
        headers = {
            "User-Agent": user_agent,
            "Host": "zhidao.baidu.com",
            #"Referer":"https://zhidao.baidu.com/list?cid=103111&tag=%C3%F1%BC%E4%BD%E8%B4%FB"
        }
        for link in link_list:
            yield scrapy.Request(link, headers=headers,cookies=cookies,callback=self.parse_question)


    def parse_question(self,response):
        question = response.xpath('//h1[@accuse="qTitle"]/span/text()').extract_first("")
        if question:
            data = response.xpath('string(//div[@id="wgt-ask"]/div[@accuse="qContent"]|//pre[@class="line mt-10 q-supply-content"])')
            answer = response.xpath('//div[@class="line content"]/div[1]/span/text()').extract_first("")
            pre_content = data.xpath("string(.)").extract_first("")
            if pre_content:
                question = pre_content.strip()
            item = LawdataspiderItem()
            item['question']=question.strip()
            item['answer']=answer.strip()
            yield item
