# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Item

import redis


class BookPipeline(object):
    review_rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def process_item(self, item, spider):
        rating = item.get('review_rating')
        if rating:
            item['review_rating'] = self.review_rating_map[rating]

        return item


class RedisPipeline(object):
    def open_spider(self, spider):
        db_host = spider.settings.get('REDIS_HOST', 'localhost')
        db_port = spider.settings.get('REDIS_PORT', 6379)
        db_index = spider.settings.get('REDIS_DB_INDEX', 0)

        # 連接資料庫
        self.db_connect = redis.StrictRedis(host=db_host, port=db_port, db=db_index)
        self.item_index = 0

    def close_spider(self, spider):
        # 關閉連接
        self.db_connect.connection_pool.disconnect()

    def process_item(self, item, spider):
        self.insert_db(item)

        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)

        self.item_index += 1
        # 將資料以 Hash 類型(雜湊) 儲存到 Redis 中
        self.db_connect.hmset('book:{}'.format(self.item_index), item)
