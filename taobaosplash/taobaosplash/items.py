# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

from scrapy.loader.processors import TakeFirst,MapCompose,Compose
from scrapy.loader import ItemLoader

def handle_goodUrl(value):
    return "https://detail.tmall.com/item.htm?id="+value.strip()


def handle_add_value(value):
    return "http:"+value.strip()


def handle_strip(value):
    return value.strip()


def handle_market_price(value):
    if "-" in value:
        return value.split("-")[0].strip()
    return value.strip()


def return_value(value):
    return value


def handle_freight(value):
    if not value:
        return []
    freight_str = value[0]
    freights = []
    if "免运费" in freight_str or "快递包邮" in freight_str:
        return "0.00"
    elif "EMS" in freight_str:
        #快递: 0.00 EMS: 15.00
        freight_list = freight_str.strip().split(" ")
        freight_dict = {}
        freight_dict["express"] = freight_list[1]
        freight_dict["EMS"] = freight_list[-1]
        freights.append(freight_dict)
        return freights
    else:
        return freight_str.strip().split(" ")[-1]


def handle_stock(value):
    return re.sub("\D","",value)


def handle_all_attributes(values):
    attributeslist = []
    for value in values:
        #材质成分: 粘胶纤维(粘纤)54.7% 聚酯纤维45.3%
        attributes = value.split(":")
        attribute = {}
        attribute['name'] = attributes[0].strip()
        attribute['value'] = attributes[1].strip()
        attributeslist.append(attribute)
    return attributeslist


class TaobaoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class TaobaosplashItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 产品ID
    id = scrapy.Field(
        input_processor = MapCompose(handle_strip)
    )
    # 产品类别
    productKeyWord = scrapy.Field()
    #产品原详情链接
    url = scrapy.Field(
        input_processor=MapCompose(handle_goodUrl)
    )
    #产品封面，用于搜款网进行搜索
    imageUrl = scrapy.Field(
        input_processor=MapCompose(handle_add_value)
    )
    #产品价格
    true_price = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    #店铺名称
    store_name = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    #店铺地址
    store_address = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    #店铺ID
    store_id = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    #产品名称
    title = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    #库存
    stock = scrapy.Field(
        input_processor=MapCompose(handle_stock)
    )
    # 颜色
    color = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    #尺码
    size = scrapy.Field(
        output_processor=MapCompose(handle_strip)
    )
    #产品图片列表
    images = scrapy.Field(
        output_processor=MapCompose(handle_add_value)
    )
    #运费
    freight = scrapy.Field(
        output_processor=Compose(handle_freight)
    )
    #货号
    no = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    #产品市场价
    market_price = scrapy.Field(
        input_processor=MapCompose(handle_market_price)
    )
    #产品属性
    all_attributes = scrapy.Field(
        output_processor=Compose(handle_all_attributes)
    )
    #产品属性组合(skus)
    combination = scrapy.Field()
    #是否在搜款网搜过的标记
    isSearch = scrapy.Field()
    #是否是天猫店
    isTianMao = scrapy.Field()
    pass

