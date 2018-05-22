# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
from .settings import redis_db
import hashlib


redis_openlaw_dict = "openlaws_title"

class DuplicatePipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        hl = hashlib.md5()
        hl.update(title.encode(encoding='utf-8'))
        md5=hl.hexdigest()
        if redis_db.sismember(redis_openlaw_dict,md5):
             raise DropItem("Duplicate item found:%s" % item)
        else:
            redis_db.sadd(redis_openlaw_dict,md5)
        return item



class OpenlawspiderPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls, settings):
        dbparam = dict(
            host=settings['HOST'],
            user=settings['USER'],
            password=settings['PASSWORD'],
            database=settings['DATABASE'],
            port=settings['PORT'],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparam)
        return cls(dbpool)


    def process_item(self, item, spider):
        # 通过twisted异步池进行mysql数据库的写入
        query = self.dbpool.runInteraction(self.do_insert_wenshulaw, item)
        # 处理插入的错误
        query.addErrback(self.handle_error)
        return item


    def handle_error(self, failure, item, spider):
        print(failure)


    def do_insert_wenshulaw(self, cursor, item):
        try:
            title = item['title']
            content = item['content']
            insert_sql = "INSERT INTO wenshu(title,content) VALUES (\'%s\',\'%s\')"%(title,content)
            cursor.execute(insert_sql)
            print('---------------wenshu存储到MySQL成功--------------')
            return item
        except Exception as e:
            print(e)
