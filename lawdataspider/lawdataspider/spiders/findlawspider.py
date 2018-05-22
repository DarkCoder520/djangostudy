# -*- coding: utf-8 -*-
import scrapy
import re
import time,hashlib
from lawdataspider.items import LawdataspiderItem
from lawdataspider.settings import redis_db


class FindlawspiderSpider(scrapy.Spider):
    name = 'findlawspider'
    allowed_domains = ['china.findlaw.cn']
    #http://china.findlaw.cn/ask/browse_t01_page2/
    start_urls = ['http://china.findlaw.cn/ask/p65_d201702_t00_page1/','http://china.findlaw.cn/ask/p24_d201702_t00_page1/','http://china.findlaw.cn/ask/p16_d201702_t00_page1/']

    # divorce_list = ["离婚"]#http://china.findlaw.cn/ask/p65_d201801_t01_page1/
    # jiedai_list = ["交通事故"]#http://china.findlaw.cn/ask/p24_d201801_t01_page1/
    # traffic_tag_list= ["债务债权"]#http://china.findlaw.cn/ask/p16_d201801_t01_page1/
    #'http://china.findlaw.cn/ask/'+id+'_d201801_t01_page'+page


    def parse(self, response):
        aid = re.findall(".*(p\d+)_.*",response.url)[0]
        link_list = response.xpath('//li[@class="list-item"]/div/a/@href').extract()
        for link in link_list:
            yield scrapy.Request(link, callback=self.parse_findlaw)


        next_page_list = response.xpath('//div[@class="common-pagination"]/a/@href').extract()
        if next_page_list:
            next_page_link = next_page_list[-1]
            pageNum_list = re.findall(".*_page(\d+).*", next_page_link)
            pageNum = int(pageNum_list[0])
            # 月份 m = t.tm_mon
            t = time.localtime(time.time() - 15*30*24*3600)
            #日期
            d = time.strftime("%Y%m", t)
            for page in range(1,pageNum+1):
                url = 'http://china.findlaw.cn/ask/'+str(aid)+'_d'+d+'_t00_page'+str(page)
                yield scrapy.Request(url,callback=self.parse_detail)


    def parse_detail(self,response):
        link_list = response.xpath('//li[@class="list-item"]/div/a/@href').extract()
        for link in link_list:
            yield scrapy.Request(link, callback=self.parse_findlaw)


    def parse_findlaw(self,response):
        lawitem = LawdataspiderItem()
        question = response.xpath('//div[@class="w880 float-left"]/div[1]/h1/text()').extract_first("")
        detail = response.xpath('//div[@class="w880 float-left"]/div[1]/p[@class="q-detail"]/text()').extract_first("")
        if detail:
            question = detail
        data = response.xpath('//div[@class="w880 float-left"]/div[contains(@class,"best-answer badge badge-best")]/div[2]/div[2]')
        answer = data.xpath("string(.)").extract_first("")
        if question:
            lawitem['question'] = question.strip()
            lawitem['answer'] = answer.strip()
            yield lawitem


