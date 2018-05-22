# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import lawdataspider.settings

from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
from lawdataspider.settings import redis_db
import hashlib


redis_baidudata_dict = "baidulawquestion"
redis_findlawdata_dict = "findlawquestion"


class DuplicatePipeline(object):
    def process_item(self, item, spider):
        if spider.name == "baidulawspider":
            question = item['question']
            hl = hashlib.md5()
            hl.update(question.encode(encoding='utf-8'))
            md5=hl.hexdigest()
            if redis_db.hexists(redis_baidudata_dict,md5):
                 raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_baidudata_dict,md5,md5)

        elif spider.name=="findlawspider":
            question = item['question']
            answer = item['answer']
            hl = hashlib.md5()
            hl.update(question.encode(encoding='utf-8'))
            question_md5 = hl.hexdigest()
            hl.update(answer.encode(encoding='utf-8'))
            answer_md5 = hl.hexdigest()
            if redis_db.hexists(redis_findlawdata_dict, question_md5):
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_findlawdata_dict, question_md5, answer_md5)
        return item



class LawdataspiderByTwistedPipeline(object):
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
        if spider.name =="baidulawspider":
            # 通过twisted异步池进行mysql数据库的写入
            query = self.dbpool.runInteraction(self.do_insert_baidulaw, item)
        elif spider.name == "findlawspider":
            # 通过twisted异步池进行mysql数据库的写入
            query = self.dbpool.runInteraction(self.do_insert_findlaw, item)
            # 处理插入的错误
        query.addErrback(self.handle_error)
        return item


    def handle_error(self, failure, item, spider):
        print(failure)


    def do_insert_baidulaw(self, cursor, item):
        try:
            question = item['question']
            answer = item['answer']
            insert_sql = "INSERT INTO baidu_know(question,answer) VALUES (\'%s\',\'%s\')"%(question,answer)
            cursor.execute(insert_sql)
            print('---------------baidulaw存储到MySQL成功--------------')
            return item
        except Exception as e:
            print(e)


    def do_insert_findlaw(self, cursor, item):
        try:
            question = item['question']
            answer = item['answer']
            insert_sql = "INSERT INTO findlaw(question,answer) VALUES (\'%s\',\'%s\')"%(question,answer)
            cursor.execute(insert_sql)
            print('---------------findlaw存储到MySQL成功--------------')
            return item
        except Exception as e:
            print(e)


