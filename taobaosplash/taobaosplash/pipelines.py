# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from taobaosplash.settings import MONGO_URL,MONGO_DB,MONGO_COLLECTION

class TaobaosplashPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=MONGO_URL, port=27137)
        self.db = client[MONGO_DB]
        self.tbCollection = self.db[MONGO_COLLECTION]


    def process_item(self, item, spider):
        try:
            item = dict(item)
            if self.tbCollection.insert(item) and item['combination']:
                print('---------------存储到MongoDB成功--------------')
        except Exception as e:
            print(e)
        return item