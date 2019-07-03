import json

import redis

ITEM_KEY = 'books:items'


def process_item(item):
    # 增加處理資料的程式
    print(item)


def main():
    db_host = '192.168.157.132'
    db_port = 6379
    db = redis.StrictRedis(host=db_host, port=db_port)

    for _ in range(db.llen(ITEM_KEY)):
        data = db.lpop(ITEM_KEY)
        item = json.loads(data.decode('utf8'))
        process_item(item)


if __name__ == '__main__':
    main()
