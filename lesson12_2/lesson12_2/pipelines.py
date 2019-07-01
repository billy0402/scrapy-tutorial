# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi

import MySQLdb


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


class MySQLPipeline(object):
    def open_spider(self, spider):
        host = spider.settings.get('MYSQL_DB_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_DB_PORT', 3306)
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        user = spider.settings.get('MYSQL_DB_USER', 'root')
        password = spider.settings.get('MYSQL_DB_PASSWORD', 'root')

        # self.db_connect = MySQLdb.connect(host=host, port=port, db=db,
        #                                   user=user, password=password, charset='utf8')
        # self.db_cursor = self.db_connect.cursor()
        self.dbpool = adbapi.ConnectionPool('MySQLdb', host=host, db=db,
                                            user=user, password=password, charset='utf8')

    def close_spider(self, spider):
        # self.db_connect.commit()
        # self.db_connect.close()
        self.dbpool.close()

    def process_item(self, item, spider):
        # self.insert_db(item)
        self.dbpool.runInteraction(self.insert_db, item)

        return item

    # def insert_db(self, item):
    def insert_db(self, transaction, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock']
        )

        sql = 'INSERT INTO books VALUES (%s, %s, %s, %s, %s, %s)'
        # self.db_cursor.execute(sql, values)
        transaction.execute(sql, values)

        # self.db_connect.commit()
