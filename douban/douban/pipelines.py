# -*- coding: utf-8 -*-
import pymysql
from scrapy.exceptions import DropItem
import pymongo
from .items import DoubanUpcomingItem, DoubannowplayingItem, DoubanlistwpItem


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):

    def __init__(self):
        self.conn = None
        self.cur = None
        self.limit = 100

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            db='douban',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, DoubanUpcomingItem):
            sql = "INSERT INTO `upcoming`(upcoming_release_time,upcoming_title,upcoming_kind,upcoming_area,upcoming_love_num) VALUES ('%s','%s','%s','%s','%s')" % (
                item['upcoming_release_time'], item['upcoming_title'], item['upcoming_kind'], item['upcoming_area'],
                item['upcoming_love_num'])
            self.cur.execute(sql)
            self.conn.commit()
            return item

        if isinstance(item, DoubanlistwpItem):
            if item['list_desc']:
                if len(item['list_desc']) > self.limit:
                    item['list_desc'] = item['list_desc'][0:self.limit].rstrip() + "..."

            sql = "INSERT INTO `top_movie`(list_directors,list_cover,list_rate,list_url,list_casts,list_title,list_rank,list_desc) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                item['list_directors'], item['list_cover'], item['list_rate'], item['list_url'], item['list_casts'],
                item['list_title'],
                item['list_rank'], pymysql.escape_string(item['list_desc']))
            self.cur.execute(sql)
            self.conn.commit()
            return item


class MongoPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.limit = 100

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, DoubannowplayingItem):
            if item['desc']:
                if len(item['desc']) > self.limit:
                    item['desc'] = item['desc'][0:self.limit].rstrip() + "..."
                    self.db[self.collection_name].insert(dict(item))
                    return item
