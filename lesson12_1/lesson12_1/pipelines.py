# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


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


class SQLitePipeline(object):
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'scrapy_default.db')

        # 連接資料庫，獲得 Connection 物件
        self.db_connect = sqlite3.connect(db_name)
        # 建立 Cursor 物件，用來執行 SQL 敘述
        self.db_cursor = self.db_connect.cursor()

    def close_spider(self, spider):
        # 儲存變更，commit 後資料才被實際寫入資料庫
        self.db_connect.commit()
        # 關閉連接
        self.db_connect.close()

    def process_item(self, item, spider):
        self.insert_db(item)

        return item

    def insert_db(self, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock']
        )

        sql = 'INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)'
        # 插入一筆資料
        self.db_cursor.execute(sql, values)

        # 每插入一筆就 commit 一次會影響效率
        # self.db_connect.commit()
