# scrapy-tutorial

## environment
- [macOS 10.14.6](https://www.apple.com/tw/macos/mojave/)
- [PyCharm 2019.2.3](https://www.jetbrains.com/pycharm/)
- [Python 3.7.4](https://www.python.org/)
- [Scrapy 1.6.0](https://github.com/scrapy/scrapy)

## [Scrapy](https://scrapy.org/)
```shell
# install
$ pipenv install scrapy

# create new project
$ scrapy startproject <project name>
# create spider file
$ scrapy genspider <spider name> <domain>

# tree project
$ pipenv install tree
$ tree .
Scrapy/
├── <project name>
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       └── spiders.py
└── scrapy.cfg

# crawler(-t: file type, -o: file path)
$ scrapy crawl books -t csv -o books.csv --nolog
# %(name)s: spider name, %(time)s: file create time
$ scrapy crawl books -o 'export_data/%(name)s/%(time)s.csv'
# see result
$ sed -n '2,$p' books.csv | cat -n
# get file head 5 lines
$ head -5 books.csv

# open scrapy shell
$ scrapy shell <url>
# open view response in a browser
$ view(response)
```

## selector
- [XPath](https://www.w3.org/TR/xpath/all/)
- [XPath Syntax](https://www.w3schools.com/xml/xpath_syntax.asp)
- [CSS](https://www.w3.org/TR/selectors-3/)
- [CSS Selector](https://www.w3schools.com/cssref/css_selectors.asp)

## [tesseract](https://github.com/tesseract-ocr/tesseract)
```shell
$ brew install tesseract
$ brew install tesseract-lang # 語言包
```

## Browser Cookies Middleware
```python
# scrapy shell
from scrapy import Request
url = 'https://github.com/settings/profile'     
fetch(Request(url, meta={'cookiejar': 'chrome'}))
view(response)
```

## [Splash](https://splash.readthedocs.io/en/stable/)
```shell
$ docker pull scrapinghub/splash
$ docker run --name mysplash -p 8050:8050 -p 8051:8051 -d scrapinghub/splash 
```

## HTTP Proxy test
```shell
# HTTP Proxy enviroment variable setup 
$ export http(s)_proxy="http(s)://username:password@proxy_ip:proxy_port"
$ scrapy shell
```
```python
import json
import base64
from scrapy import Request

url = 'https://httpbin.org/ip'
proxy = 'proxy_ip:proxy_port'
user = 'username'
password = 'password'
auth = '{}:{}'.format(user, password).encode('utf8')
request = Request(url, meta={'proxy': proxy})
request.headers['Proxy-Authorization'] = b'Basic' + base64.b64encode(auth)
fetch(request)
json.loads(response.text)
```

## free Proxy
- [Proxy List](http://proxy-list.org/english/index.php)
- [Free Proxy List](https://free-proxy-list.net/)
- [西刺免費代理IP](https://www.xicidaili.com/)
- [Proxy 360](http://www.proxy360.cn/default.aspx)
- [快代理](https://www.kuaidaili.com/)

## SQLite
```shell
$ sqlite3 scrapy.db
$ .exit
```
```sqlite
CREATE TABLE books (
    upc           CHAR(16) NOT NULL PRIMARY KEY,
    name          VARCHAR(256) NOT NULL,
    price         VARCHAR(16) NOT NULL,
    review_rating INT,
    review_num    INT,
    stock         INT
);
SELECT * FROM books;
```

## [MySQL(docker)](https://hub.docker.com/_/mysql)
### [mysqlclient](https://github.com/PyMySQL/mysqlclient-python)
```shell
$ docker run --name mymysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 -d mysql:5.7.26
$ docker exec -it mymysql bash
$ mysql -h 127.0.0.1 -u root -p
$ brew install mysql-connector-c
$ pip install mysqlclient
```
```mysql
CREATE DATABASE scrapy_db CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE scrapy_db;
CREATE TABLE books (
    upc           CHAR(16) NOT NULL PRIMARY KEY,
    name          VARCHAR(256) NOT NULL,
    price         VARCHAR(16) NOT NULL,
    review_rating INT,
    review_num    INT,
    stock         INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SELECT * FROM books;
```

## [MongoDB(docker)](https://hub.docker.com/_/mongo)
```shell
# setup MongoDB docker
$ docker images
$ docker rmi <IMAGE ID>
$ docker pull mongo
$ docker run --name mymongo -p 27017:27017 -d mongo
$ docker exec -it mymongo bash
$ mongo

# MongoDB command
$ use scrapy_data
$ db.getCollectionNames()
$ db.books.count()
$ db.books.find()
$ db.books.drop()
```

## [redis](https://redis.io/)
### [redis(docker)](https://hub.docker.com/_/redis/)
```shell
$ docker run --name myredis -p 6379:6379 -d redis
$ docker exec -it myredis bash
$ redis-cli
```
### redis server(Ubuntu)
```shell
# 安裝 redis-server
$ sudo apt-get install redis-server
$ sudo service redis-server start
$ sudo service redis-server restart
$ sudo service redis-server stop

# 查詢服務
$ sudo apt install net-tools
$ netstat -ntl

# 設定連線限制
$ sudo vi /etc/redis/redis.conf
# 接受任意 IP 請求
# bind 127.0.0.1 > bind 0.0.0.0

# 取得 IP
$ ifconfig
# 使用 -h 參數指定主機 ip
$ redis-cli -h <host ip>
# 測試連接資料庫是否成功
$ PING
# scrapy-redis 設定起始爬取點
$ lpush books:start_urls 'http://books.toscrape.com/'
```
### redis-cli
```shell
# KEYS 鍵值
$ KEYS * # 取得 redis 中的所有 key 值
$ KEYS key:* # 取得 book 中的所有 key 值

# String 字串
$ SET key value # 設定字串 key 的值
$ GET key # 取得字串 key 的值
$ DEL key # 刪除字串 key

# List 列表
$ LPUSH key [value] # 在列表 key 左端插入一個或多個值
$ RPUSH key [value] # 在列表 key 右端插入一個或多個值
$ LPOP key # 從列表 key 左端取出一個值
$ RPOP key # 從列表 key 右端取出一個值
$ LINDEX key index # 取得列表 key 中 index 位置的值
$ LRANGE key start end # 取得列表 key 中位置從 start 到 end 範圍的值
$ LLEN key 取得列表 key 的長度

# Hash 雜湊
$ HSET key field value # 將雜湊 key 中的 field 欄位設定值為 value
$ HDEL key [field] # 刪除雜湊 key 中的一個或多個欄位
$ HGET key field 取得雜湊 key 中的 field 欄位的值
$ HGETALL key 取得雜湊 key 中的所有欄位和值
$ HGETALL key:field # 取得雜湊 key 中的欄位為 field 的值

# Set 集合
$ SADD key [member] # 向集合 key 中增加一個或多個成員
$ SREM key [member] # 向集合 key 中刪除一個或多個成員
$ SMEMBERS key # 取得集合 key 中的所有成員
$ SCARD key # 取得集合 key 中的成員數量
$ SISMEMBER key member # 判斷 member 是否是集合 key 的成員

# ZSet 有序集合
$ ZADD key [score member] # 向有序集合 key 中增加一個或多個成員
$ ZREM key [member] # 向有序集合 key 中刪除一個或多個成員
$ ZRANGE key start stop # 取得有序集合 key 中位置從 start 到 end 的所有成員
$ ZRANGEBYSCORE key min max # 取得有序集合 key 中分數從 mix 到 max 的所有成員
```