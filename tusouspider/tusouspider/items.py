# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose,TakeFirst,Compose
from scrapy.loader import ItemLoader


def handle_stallDetail(results):
    detail = {}
    for result in results:
        #newstr = new_result.xpath("./string(.)")[0]
        str = result.strip()
        if "排行" in str:
            productRank = re.sub('\D','',str)
            detail['productRank'] = productRank
        elif "旺旺" in str:
            detail['wwName'] = str.split('：')[-1].strip()
        elif "商品" in str:
            productCount = re.sub('\D', '', str)
            detail['productCount'] = productCount
        elif "电话" in str:
            detail['mobile'] = str.split('：')[-1].strip()
            pass
        elif "微信" in str:
            detail['weixi'] = str.split('：')[-1].strip()
        elif "QQ" in str:
            detail['qq'] = str.split('：')[-1].strip()
        elif "产地" in str:
            detail['produceAddr'] = str.split('：')[-1].strip()
        elif "地址" in str:
            detail['address'] = str.split('：')[-1].strip()
        else:
            pass
    return detail


def handle_strip(value):
    return value.strip()


def handle_price(value):
    price_length = len(value)
    if price_length > 1:
        value = value[:-1]
        return "".join(value).strip()
    return "".join(value).strip()


def handle_color(value):
    color_list = []
    for color_str in value:
        if "颜色分类" in color_str:
            color_list.append(color_str.split(":")[1].strip())
    return color_list


def handle_shopId(values):
    value = values[0]
    return value.split('/')[-1]


def return_value(value):
    return value


def join_value(value):
    return "http:"+value


class TusouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class TusouspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(
        input_processor =MapCompose(handle_strip)
    )
    goodUrl = scrapy.Field()

    parentId = scrapy.Field()

    imageUrl = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    price = scrapy.Field(
        input_processor=Compose(handle_price),
    )
    shopName = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    shopId = scrapy.Field(
        output_processor=Compose(handle_shopId)
    )
    allRule = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    allColor = scrapy.Field(
        output_processor=Compose(handle_color)
    )
    allPicUrl = scrapy.Field(
        input_processor = MapCompose(join_value),
        output_processor=MapCompose(return_value)
    )
    stallDetail = scrapy.Field(
        output_processor = Compose(handle_stallDetail)
    )
    pass
