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
    name = 'dressspider'
    allowed_domains = ['www.taobao.com','detail.tmall.com','s.taobao.com']
    start_urls = ['http://www.taobao.com/']

    # def __init__(self):
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.add_argument('--headless')
    #     self.browser = webdriver.Chrome(executable_path=r'D:\chromedriver\chromedriver.exe',chrome_options=chrome_options)
    #     #self.browser = webdriver.PhantomJS(executable_path=r"D:\phantomjs\phantomjs.exe")
    #     self.wait = WebDriverWait(self.browser, 10)
    #     pass

    #'打底衫','夹克'
    '''
        local page = splash.args.page
        if (page > 1) then:
            assert(splash:go(splash.args.url))
            input = assert(splash:select(#mainsrp-pager div.form input.input.J_Input))
            input:send_text(splash.args.page)
            submit = assert(splash:select('#mainsrp-pager div.form span.btn.J_Submit'))
            submit:mouse_click()
            splash:wait(splash.args.wait)
            return splash:html()
        end
    '''
    '''
        request:set_proxy{'http://http-dyn.abuyun.com', '9020', username='HOL01VVM80BOJ59D', password='85FE83F49EE3EFEB', type='HTTP'}
        assert(splash:go("https://s.taobao.com/search?q=甜美风"))
        splash:wait(0.5)
        items = splash:select('#mainsrp-itemlist div.items .item')
        if items then:
            item=items[0]
            item:mouse_click()
            splash:wait(0.5)
            return splash:html()
        end
    '''
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
        for page in range(3,4):
            for keyword in keyWordList:
                url = 'https://s.taobao.com/search?q=' + quote(keyword)
                #url = 'http://httpbin.org/get'
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
        splash_args = {'wait': 1,'lua_source': script,'cookies':cookies}
        for i in range(0,len(items)):
            item_loader = TaobaoItemLoader(TaobaosplashItem(),response=response)
            item_loader.nested_css(path).add_css('id','div[data-index="'+str(i)+'"] .title .J_ClickStat::attr(data-nid)')
            item_loader.nested_css(path).add_css('imageUrl','div[data-index="'+str(i)+'"] .pic .img::attr(data-src)')
            item_loader.nested_css(path).add_css('store_id','div[data-index="'+str(i)+'"] .shop .J_ShopInfo::attr(data-userid)')
            item_loader.nested_css(path).add_css('true_price','div[data-index="'+str(i)+'"] div[class*="price"] strong::text')
            item_loader.nested_css(path).add_css('store_name','div[data-index="'+str(i)+'"] .shop a span:nth-child(2)::text')
            item_loader.nested_css(path).add_css('store_address','div[data-index="'+str(i)+'"] .shop div.location::text')
            is_tianmao = len(items[i].css("span.icon-service-tianmao"))
            item_loader.add_value('url',item_loader.get_output_value('id'))
            item_loader.add_value('isTianMao',is_tianmao)
            item_loader.add_value('productKeyWord',keyword)
            goodItem = item_loader.load_item()
            metas = {'goodItem':goodItem}
            url = item_loader.get_output_value('url')
            yield SplashRequest(url, self.parse_product_by_splash,endpoint='execute',meta=metas, headers=headers,
                                 args=splash_args)
            #yield scrapy.Request("https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9F02wVS&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F", self.parse_product_by_selenium, meta=metas, headers={'User-Agent': user_agent},dont_filter=True)


    def parse_product_by_splash(self,response):
        goodItem = response.meta['goodItem']
        is_tianmao = goodItem['isTianMao']
        #通过itemloader方式获取的字段
        item_loader = TaobaoItemLoader(TaobaosplashItem(), response=response)
        item_loader.add_xpath('title','//div[@class="tb-property"]/div/div[1]/h1/text()|//div[@class="tb-item-info-r"]/div/div/div[1]/h3/text()')
        item_loader.add_xpath('stock','//div[@class="tb-skin"]/div/dl[3]/dd/em/text()|//div[@class="tb-skin"]/dl[3]/dd/em/span/text()')
        item_loader.nested_xpath('//div[@id="J_PostageToggleCont"]/p/span|//div[@id="J_LogisticInfo"]/div[2]/span').add_xpath('freight','string(.)')
        item_loader.add_xpath('market_price','//div[@class="tm-fcs-panel"]/dl[@id="J_StrPriceModBox"]/dd/span/text()|//div[@class="tb-wrap tb-wrap-newshop"]/ul[1]/li[1]/div/strong/em[2]/text()')
        item_loader.add_xpath('size','//div[@class="tb-skin"]/div/dl[1]/dd/ul/li/a/span/text()|//div[@class="tb-skin"]/dl[1]/dd/ul/li/a/span/text()')
        item_loader.add_xpath('images','//div[@class="tb-gallery"]/div[2]/div/ul/li/a/img/@src|//div[@class="tb-gallery"]/ul/li/div/a/img/@src')
        item_loader.add_xpath('all_attributes','//div[@class="sub-wrap"]/div[@id="attributes"]/ul/li/text()|//div[@id="mainwrap"]/div[@id="attributes"]/div/ul/li/text()')

        #通过xpath规则来获取字段
        #color_list = response.xpath('//div[@class="tb-skin"]/div/dl[2]/dd/ul/li/a/span/text()|//div[@class="tb-skin"]/dl[2]/dd/ul/li/a/span/text()').extract()
        color_id = response.xpath('//div[@class="tb-skin"]/div/dl[2]/dd/ul/li/@data-value|//div[@class="tb-skin"]/dl[2]/dd/ul/li/@data-value').extract()
        size_id = response.xpath('//div[@class="tb-skin"]/div/dl[1]/dd/ul/li/@data-value|//div[@class="tb-skin"]/dl[1]/dd/ul/li/@data-value').extract()

        #color字段的获取
        link_items = response.xpath('//div[@class="tb-skin"]/div/dl[2]/dd/ul/li | //div[@class="tb-skin"]/dl[2]/dd/ul/li')
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

        # color = []
        # for i in range(0,len(color_list)):
        #     if not links:
        #         color.append("")
        #     else:
        #         linkstr = links[i]
        #         link = re.findall(".*url\((.*?\.jpg).*", linkstr)[0]
        #         color.append("http:"+link)
        # color_link = dict(zip(color_list,color))
        # color.clear()
        # for name,value in color_link.items():
        #     color_dict = {}
        #     color_dict['name'] = name
        #     color_dict['value'] = value
        #     color.append(color_dict)

        #货号字段的获取
        all_attributes = item_loader.get_output_value('all_attributes')
        no = ""
        for attributes in all_attributes:
            if attributes['name'] in "货号":
                no = attributes['value']
                break

        #各种属性组合字段的获取combination
        size_list = item_loader.get_output_value('size')
        size_dict = dict(zip(size_id,size_list))
        color_dict = dict(zip(color_id,color_list))
        market_price = item_loader.get_output_value('market_price')
        true_price = goodItem['true_price']
        rate = 0
        if true_price and market_price:
            true_price = float(true_price)
            market_price = float(market_price)
            rate = round(true_price/market_price,3)

        if is_tianmao:
            combination = tianmaodata_json(response.text, rate)
        else:
            combination = taobaodata_json(response.text, size_dict, color_dict, rate)

        #将获取的字段加入到item_loader中
        item_loader.add_value('no', no)
        item_loader.add_value('color', color)
        item_loader.add_value('combination',combination)
        item_loader.add_value('isSearch',0)
        secItem = item_loader.load_item()
        newGoodItem = dict(goodItem, **secItem)
        yield newGoodItem


    def parse_product_by_selenium(self,response):
            goodItem = response.meta['goodItem']
            good_url = goodItem['url']
            try:
                self.browser.get(good_url)
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#detail .tb-skin')))
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.tb-gallery .tb-thumb')))
                html = self.browser.page_source
                doc = etree.HTML(html)
                title = doc.xpath('string(//div[@class="tb-property"]/div/div[1]/h1/text()|//div[@class="tb-item-info-r"]/div/div/div[1]/h3)').strip()
                stock = ""
                stock_list = doc.xpath('//div[@class="tb-skin"]/div/dl[3]/dd/em/text()|//div[@class="tb-skin"]/dl[3]/dd/em/span/text()')
                if stock_list:
                    stock = handle_stock(stock_list[0])
                freight = handle_freight([doc.xpath('string(//div[@id="J_PostageToggleCont"]/p|//div[@id="J_LogisticInfo"]/div[2]/span)')])
                if not freight:
                    freight = "0.00"
                market_price = ""
                market_price_list = doc.xpath('//div[@class="tm-fcs-panel"]/dl[@id="J_StrPriceModBox"]/dd/span/text()|//div[@class="tb-wrap tb-wrap-newshop"]/ul[1]/li[1]/div/strong/em[2]/text()')
                if market_price_list:
                    market_price = handle_market_price(market_price_list[0])
                size = [size_str.strip() for size_str in doc.xpath('//div[@class="tb-skin"]/div/dl[1]/dd/ul/li/a/span/text()|//div[@class="tb-skin"]/dl[1]/dd/ul/li/a/span/text()')]
                images = ["http:"+image for image in doc.xpath('//div[@class="tb-gallery"]/div[2]/div/ul/li/a/img/@src|//div[@class="tb-gallery"]/ul/li/div/a/img/@src')]
                all_attributes = handle_all_attributes(doc.xpath('//div[@class="sub-wrap"]/div[@id="attributes"]/ul/li/text()|//div[@id="mainwrap"]/div[@id="attributes"]/div/ul/li/text()'))
                color_id = doc.xpath('//div[@class="tb-skin"]/div/dl[2]/dd/ul/li/@data-value|//div[@class="tb-skin"]/dl[2]/dd/ul/li/@data-value')
                size_id = doc.xpath('//div[@class="tb-skin"]/div/dl[1]/dd/ul/li/@data-value|//div[@class="tb-skin"]/dl[1]/dd/ul/li/@data-value')

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
                size_dict = dict(zip(size_id, size))
                color_dict = dict(zip(color_id, color_list))
                true_price = goodItem['true_price']
                rate = 0
                if true_price and market_price:
                    true_price = float(true_price)
                    market_price = float(market_price)
                    rate = round(true_price / market_price, 3)
                combination = tianmaodata_json(html, rate)
                if not combination:
                    combination = taobaodata_json(html, size_dict, color_dict, rate)

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


