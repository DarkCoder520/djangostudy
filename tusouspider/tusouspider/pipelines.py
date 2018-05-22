# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from tusouspider.settings import MONGO_URL,MONGO_DB,MONGO_COLLECTION,MONGO_SOUKUANWANG_COLLECTION
from twisted.enterprise import adbapi

class TusouspiderPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=MONGO_URL, port=27137)
        self.db = client[MONGO_DB]
        self.tbCollection = self.db[MONGO_SOUKUANWANG_COLLECTION]
        self.skwCollection = self.db[MONGO_COLLECTION]

    def process_item(self, item, spider):
        try:
            item = dict(item)
            if self.tbCollection.insert(item):
                parent_id = item['parentId']
                self.skwCollection.update({"_id":parent_id},{"$set":{"isSearch":1}})
                print('---------------存储到MongoDB成功--------------')
        except Exception as e:
            print(e)
        return item



class TusouspiderByTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparam = dict(
            host=settings['MONGO_URL'],
            db=settings['MONGO_DB'],
            charset="utf8",
            cursorclass=pymongo.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymongo", **dbparam)
        return cls(dbpool)


    def process_item(self, item, spider):
        # 通过twisted异步池进行mysql数据库的写入
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理插入的错误
        query.addErrback(self.handle_error)
        return item


    def handle_error(self, failure, item, spider):
        print(failure)


    def do_insert(self, cursor, item):

        try:
            item = dict(item)
            if cursor.insert(item):
                parent_id = item['parentId']
                cursor.update({"_id":parent_id},{"$set":{"isSearch":1}})
                print('---------------存储到MongoDB成功--------------')
        except Exception as e:
            print(e)
        return item
        cursor.execute(insert_sql, values)

