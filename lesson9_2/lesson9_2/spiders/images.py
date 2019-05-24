# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request


class ImagesSpider(scrapy.Spider):
    BASE_URL = 'http://image.so.com/zj?ch=art&sn={}&listtype=new&temp=1'
    start_index = 0

    # 限制最大下載量，防止磁碟用量過大
    MAX_DOWNLOAD_NUM = 1000

    name = 'images'
    allowed_domains = ['image.so.com']
    start_urls = [BASE_URL.format(start_index)]

    def parse(self, response):
        # 使用 json 模組解析回應結果
        infos = json.loads(response.body.decode('UTF-8'))
        # 如果 count 欄位大於0
        if infos['count'] > 0:
            # 分析所有圖片下載 url 到一個列表
            urls = [info['qhimg_url'] for info in infos['list']]
            # 指定給 item 的 'image_urls' 欄位
            yield {'image_urls': urls}

        self.start_index += infos['count']
        # 如果下載數量不足 MAX_DOWNLOAD_NUM
        if self.start_index < self.MAX_DOWNLOAD_NUM:
            # 繼續下一頁圖片資訊
            yield Request(self.BASE_URL.format(self.start_index))
