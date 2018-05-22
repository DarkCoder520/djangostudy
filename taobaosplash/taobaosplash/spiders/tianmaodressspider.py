# -*- coding: utf-8 -*-
import scrapy
import random
import json

from urllib.parse import quote
from scrapy_splash import SplashRequest
from taobaosplash.settings import USER_AGENTS
from taobaosplash.items import TaobaosplashItem
from taobaosplash.items import TaobaoItemLoader
from taobaosplash.combinationUtils import *
from lxml import etree




import multiprocessing
import pymongo

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote

from taobaosplash.items import handle_freight,handle_stock,handle_market_price,handle_all_attributes
from taobaosplash.settings import COOKIE_LISTS
'''
总结：itemloader 是按照css3选择器的语法来
'''
class DressspiderSpider(scrapy.Spider):
    name = 'tianmaodressspider'
    allowed_domains = ['www.taobao.com','detail.tmall.com','s.taobao.com']
    start_urls = ['http://www.taobao.com/']

    #def __init__(self):
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        #chrome_options=chrome_options
        #self.browser = webdriver.Chrome(executable_path=r'D:\chromedriver\chromedriver.exe')
        #self.browser = webdriver.PhantomJS(executable_path=r"D:\phantomjs\phantomjs.exe",service_args=['--ignore-ssl-errors=true','--ssl-protocol=TLSv1'])
        #self.wait = WebDriverWait(self.browser, 10)
    #    pass

    def start_requests(self):
        keyWordList = ['甜美风']
        script = '''
                 function main(splash)
                     local page = splash.args.page
                     if page>1 then
                           assert(splash:go(splash.args.url))	     
                           splash:wait(0.5)
                           input = splash:select('#mainsrp-pager div.form input.input.J_Input')
                           input:focus()
                           splash:send_text(''..page)
                           assert(splash:wait(0))
                           submit = splash:select('#mainsrp-pager div.form span.btn.J_Submit')
                           submit:mouse_click()
                           assert(splash:wait(0.5))
                           return splash:html()
                     end
                     assert(splash:go(splash.args.url))
                     splash:wait(0.5)
                     return splash:html()
                 end
        '''
        for page in range(2,3):
            for keyword in keyWordList:
                url = 'https://s.taobao.com/search?q=' + quote(keyword)
                splash_args = {
                    'page': page,
                    'wait': 0.5,
                    'lua_source': script,
                }
                metas={
                    'keyword':keyword
                }
                user_agent = random.choice(USER_AGENTS)
                yield SplashRequest(url,self.parse,endpoint='execute',meta=metas,headers={'User-Agent':user_agent},args=splash_args)


    def parse(self, response):
        keyword = response.meta['keyword']
        path = '#mainsrp-itemlist div.items'
        items = response.css('#mainsrp-itemlist div.items div[class*="item"]')
        script ='''
                function main(splash)
                    splash:init_cookies(splash.args.cookies)
                    splash:on_request(function(request)
                        request:set_proxy{'forward.xdaili.cn', '80', username='', password='', type='HTTPS'}
                    end)
                    assert(splash:go(splash.args.url))
                    assert(splash:wait(splash.args.wait))
                    return splash:html()
                end 
                '''
        orderno = "ZF20184247995dIkqrh"
        secret = "c672faf1c26c4289a997b7c1911a9bb8"
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        md5_string = hashlib.md5(string.encode("utf-8")).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        user_agent = random.choice(USER_AGENTS)
        headers = {
            'User-Agent': user_agent,
            "Proxy-Authorization": auth
        }
        cookies = json.loads(random.choice(COOKIE_LISTS))
        splash_args = {'wait': 1.5,'lua_source': script,'cookies':cookies}
        for i in range(0,len(items)):
            is_tianmao = len(items[i].css("span.icon-service-tianmao"))
            if is_tianmao:
                item_loader = TaobaoItemLoader(TaobaosplashItem(),response=response)
                item_loader.nested_css(path).add_css('id','div[data-index="'+str(i)+'"] .title .J_ClickStat::attr(data-nid)')
                item_loader.nested_css(path).add_css('imageUrl','div[data-index="'+str(i)+'"] .pic .img::attr(data-src)')
                item_loader.nested_css(path).add_css('store_id','div[data-index="'+str(i)+'"] .shop .J_ShopInfo::attr(data-userid)')
                item_loader.nested_css(path).add_css('true_price','div[data-index="'+str(i)+'"] div[class*="price"] strong::text')
                item_loader.nested_css(path).add_css('store_name','div[data-index="'+str(i)+'"] .shop a span:nth-child(2)::text')
                item_loader.nested_css(path).add_css('store_address','div[data-index="'+str(i)+'"] .shop div.location::text')
                item_loader.add_value('url',item_loader.get_output_value('id'))
                item_loader.add_value('isTianMao',is_tianmao)
                item_loader.add_value('productKeyWord',keyword)
                goodItem = item_loader.load_item()
                metas = {'goodItem':goodItem}
                url = item_loader.get_output_value('url')
                yield SplashRequest(url, self.parse_product_by_splash,endpoint='execute',meta=metas, headers=headers,
                                     args=splash_args)
                #yield scrapy.Request("https://www.tmall.com/", self.parse_product_by_selenium, meta=metas, headers={'User-Agent': user_agent},dont_filter=True)


    def parse_product_by_splash(self,response):
        goodItem = response.meta['goodItem']
        #通过itemloader方式获取的字段
        item_loader = TaobaoItemLoader(TaobaosplashItem(), response=response)
        item_loader.add_xpath('title','//div[@class="tb-property"]/div/div[1]/h1/text()')
        item_loader.add_xpath('stock','//div[@class="tb-skin"]/div/dl[3]/dd/em/text()')
        item_loader.nested_xpath('//div[@id="J_PostageToggleCont"]/p/span').add_xpath('freight','string(.)')
        item_loader.add_xpath('market_price','//div[@class="tm-fcs-panel"]/dl[@id="J_StrPriceModBox"]/dd/span/text()')
        item_loader.add_xpath('size','//div[@class="tb-skin"]/div/dl[1]/dd/ul/li/a/span/text()')
        item_loader.add_xpath('images','//div[@class="tb-gallery"]/div[2]/div/ul/li/a/img/@src')
        item_loader.add_xpath('all_attributes','//div[@id="mainwrap"]/div[@id="attributes"]/div/ul/li/text()')

        #color字段的获取
        link_items = response.xpath('//div[@class="tb-skin"]/div/dl[2]/dd/ul/li')
        color=[]
        color_list=[]
        for link_item in link_items:
            item = {}
            name = link_item.xpath("./a/span/text()").extract_first("")
            color_list.append(name)
            item['name']=name
            linkstr = link_item.xpath("./a/@style").extract_first("")
            if linkstr:
                linkstr= re.findall(".*url\((.*?\.jpg).*", linkstr)[0]
                linkstr = "http:"+linkstr
            item['link'] = linkstr
            color.append(item)

        #货号字段的获取
        all_attributes = item_loader.get_output_value('all_attributes')
        no = ""
        for attributes in all_attributes:
            if attributes['name'] in "货号":
                no = attributes['value']
                break

        #各种属性组合字段的获取combination
        market_price = item_loader.get_output_value('market_price')
        true_price = goodItem['true_price']
        rate = 0
        if true_price and market_price:
            true_price = float(true_price)
            market_price = float(market_price)
            rate = round(true_price/market_price,3)
        combination = tianmaodata_json(response.text, rate)
        #将获取的字段加入到item_loader中
        item_loader.add_value('no', no)
        item_loader.add_value('color', color)
        item_loader.add_value('combination',combination)
        item_loader.add_value('isSearch',0)
        secItem = item_loader.load_item()
        newGoodItem = dict(goodItem, **secItem)
        yield newGoodItem


    def parse_product_by_selenium(self,good_url,goodItem):
            #goodItem = response.meta['goodItem']
            #good_url = goodItem['url']
            try:
                self.browser.get(good_url)
                #self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#detail')))
                self.wait.until(
                     EC.presence_of_element_located((By.CSS_SELECTOR, '#detail .tb-skin')))
                self.wait.until(
                     EC.presence_of_element_located((By.CSS_SELECTOR, '.tb-gallery .tb-thumb-warp')))
                html = self.browser.page_source
                if not html:
                    print("tell me?ok?")
                doc = etree.HTML(html)
                title = doc.xpath('string(//div[@class="tb-property"]/div/div[1]/h1/text())').strip()
                stock = ""
                stock_list = doc.xpath('//div[@class="tb-skin"]/div/dl[3]/dd/em/text()')
                if stock_list:
                    stock = handle_stock(stock_list[0])
                freight = handle_freight([doc.xpath('string(//div[@id="J_PostageToggleCont"]/p)')])
                if not freight:
                    freight = "0.00"
                market_price = ""
                market_price_list = doc.xpath('//div[@class="tm-fcs-panel"]/dl[@id="J_StrPriceModBox"]/dd/span/text()')
                if market_price_list:
                    market_price = handle_market_price(market_price_list[0])
                size = [size_str.strip() for size_str in doc.xpath('//div[@class="tb-skin"]/div/dl[1]/dd/ul/li/a/span/text()')]
                images = ["http:"+image for image in doc.xpath('//div[@class="tb-gallery"]/div[2]/div/ul/li/a/img/@src')]
                all_attributes = handle_all_attributes(doc.xpath('//div[@id="mainwrap"]/div[@id="attributes"]/div/ul/li/text()'))

                #color字段的获取
                link_items = doc.xpath('//div[@class="tb-skin"]/div/dl[2]/dd/ul/li | //div[@class="tb-skin"]/dl[2]/dd/ul/li')
                color = []
                color_list = []
                for link_item in link_items:
                    item = {}
                    name_list = link_item.xpath("./a/span/text()")
                    name = ""
                    if name_list:
                        name = name_list[0]
                    color_list.append(name)
                    item['name'] = name
                    link_list = link_item.xpath("./a/@style")
                    linkstr = ""
                    if link_list:
                        linkstr = link_list[0]
                        if linkstr:
                            linkstr = re.findall(".*url\((.*?\.jpg).*", linkstr)[0]
                            linkstr = "http:" + linkstr
                    item['link'] = linkstr
                    color.append(item)

                # 货号字段的获取
                no = ""
                for attributes in all_attributes:
                    if attributes['name'] in "货号":
                        no = attributes['value']
                        break

                # 各种属性组合字段的获取combination
                true_price = goodItem['true_price']
                rate = 0
                if true_price and market_price:
                    true_price = float(true_price)
                    market_price = float(market_price)
                    rate = round(true_price / market_price, 3)
                combination = tianmaodata_json(html, rate)
                secItem = {}
                secItem['title'] = title
                secItem['stock'] = stock
                secItem['freight'] = freight
                secItem['market_price'] = market_price
                secItem['size'] = size
                secItem['images'] = images
                secItem['all_attributes'] = all_attributes
                if no:
                    secItem['no'] = no
                secItem['color'] = all_attributes
                secItem['combination'] = combination
                secItem['isSearch'] = 0
                newGoodItem = dict(goodItem, **secItem)
                yield newGoodItem
            except Exception as e:
                print(e)

