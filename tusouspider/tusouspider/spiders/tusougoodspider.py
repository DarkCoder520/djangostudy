# -*- coding: utf-8 -*-
import scrapy
import pymongo
import hashlib
import random
import requests
import json
import time
from urllib import parse
from tusouspider.settings import MONGO_URL,MONGO_DB,MONGO_COLLECTION,redis_db
from tusouspider.items import TusouspiderItem
from tusouspider.items import TusouItemLoader


class TusougoodspiderSpider(scrapy.Spider):
    name = 'tusougoodspider'
    allowed_domains = ['g-search1.alicdn.com','tusou.vvic.com','www.vvic.com']
    start_urls = ['https://tusou.vvic.com']

    def __init__(self):
        client = pymongo.MongoClient(host=MONGO_URL, port=27137)
        self.db = client[MONGO_DB]
        self.tbCollection = self.db[MONGO_COLLECTION]


    def start_requests(self):
        #while True:
            products = list(self.tbCollection.find({'isSearch': 0}).limit(3000))
            for product in products:
            #product = products[0]
                imageUrl = product['imageUrl']
                parent_id = product['_id']
                parmas = {
                    'url':imageUrl,
                }
                metas = {
                    'parent_id':parent_id
                }
                url = 'https://tusou.vvic.com/upload?'+parse.urlencode(parmas)
                yield scrapy.Request(url,meta=metas,dont_filter=True)


    def parse(self, response):
        parent_id = response.meta['parent_id']
        metas = {
            'parent_id': parent_id
        }
        try:
            md5json = json.loads(response.text)
            data = md5json['data']['url']
            if "509.html" in data:
                hl = hashlib.md5()
                hl.update(response.url.encode(encoding='utf-8'))
                md5 = hl.hexdigest()
                if redis_db.sismember("skwurl", md5):
                    redis_db.srem("skwurl",md5)
                yield scrapy.Request(response.url, meta=metas, callback=self.parse, dont_filter=True)
            url = 'https://tusou.vvic.com'+data
            yield scrapy.Request(url, meta=metas,callback=self.parse_imageurl)
        except Exception as e:
            print(e)


    def parse_imageurl(self, response):
        parent_id = response.meta['parent_id']
        metas = {
            'parent_id': parent_id
        }
        searchProductStr = response.css('.desc.fl h3 em::text').extract_first("")
        if searchProductStr.isdigit() and int(searchProductStr.strip()):
            product_urls = response.css('.search-sub-main div.item div.title a::attr(href)').extract()
            for product_url in product_urls:
            #url = 'https://www.vvic.com/item/8175160'
                url = parse.urljoin(response.url, product_url)
                yield scrapy.Request(url,meta=metas,callback=self.parse_product)
        else:
            self.tbCollection.update({'_id':parent_id},{'$set':{'isSearch':1}})


    def parse_product(self,response):
        parent_id = response.meta['parent_id']
        item_loader = TusouItemLoader(TusouspiderItem(),response=response)
        item_loader.add_value('goodUrl', response.url)
        item_loader.add_value('parentId', parent_id)
        item_loader.add_css('title', '.item-content.clearfix div.d-name strong::text')
        item_loader.nested_xpath('//div[@class="product-detail "]/div[@class="price-time-buyer"]/div[1]/div[@class="p-value"]/*').add_xpath('price', 'string(.)')
        item_loader.add_css('allColor', 'div.d-attr.clearfix ul li::attr(title)')
        item_loader.add_css('imageUrl', 'div.thumbnail .tb-booth.tb-pic.tb-s400 a::attr(href)')
        item_loader.add_css('shopName', '.shop-info div.shop-content  h2.shop-name span::text')
        item_loader.add_css('shopId', '.shop-info div.shop-content div.btns.clearfix a::attr(href)')
        item_loader.add_css('allRule', '.product-detail dl#j-buy li.selectSize a::text')
        item_loader.add_css('allPicUrl', 'div.thumbnail ul#thumblist div.tb-pic.tb-s60 a img::attr(src)')
        item_loader.nested_xpath('//div[contains(@class,"shop-info")]/div/ul[@class="mt10"]/li').add_xpath('stallDetail','string(.)')
        goodItem = item_loader.load_item()
        yield goodItem