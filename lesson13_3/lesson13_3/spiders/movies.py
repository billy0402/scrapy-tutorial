# -*- coding: utf-8 -*-
import json
import re
from pprint import pprint

import scrapy
from scrapy import Request


class MoviesSpider(scrapy.Spider):
    BASE_URL = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=recommend&page_limit={}&page_start={}'
    MOVIE_TAG = '豆瓣高分'
    PAGE_LIMIT = 20
    page_start = 0

    name = 'movies'
    allowed_domains = ['movie.douban.com']
    start_urls = [BASE_URL.format(MOVIE_TAG, PAGE_LIMIT, page_start)]

    def parse(self, response):
        # 使用 json 模組解析回應結果
        infos = json.loads(response.body.decode('utf8'))
        movie_infos = infos['subjects']

        # 反覆運算影片資訊列表
        for movie_info in movie_infos:
            movie_item = dict()

            # 分析 片名 和 評分，填入 item
            movie_item['片名'] = movie_info['title']
            movie_item['評分'] = movie_info['rate']

            # 分析影片頁面 url，建置 Request 發送請求，並將 item 透過 meta 參數傳遞給影片頁面解析函數
            yield Request(movie_info['url'], callback=self.parse_movie,
                          meta={'_movie_item': movie_item})

        # 如果 json 結果中包含的影片數量小於請求數量，說明沒有影片了，否則繼續搜索
        if len(movie_infos) == self.PAGE_LIMIT:
            self.page_start += self.PAGE_LIMIT
            url = self.BASE_URL.format(self.MOVIE_TAG, self.PAGE_LIMIT, self.page_start)

            yield Request(url)

    def parse_movie(self, response):
        # 從 meta 中分析已包含 片名 和 評分 資訊的 item
        movie_item = response.meta['_movie_item']

        # 取得整個資訊字串
        info = response.css('div.subject div#info').xpath('string(.)').extract_first()

        # 分析所有欄位名稱
        fields = [s.strip().replace(':', '') \
                  for s in response.css('div#info span.pl::text').extract()]

        # 分析所有欄位的值
        values = [re.sub('\s+', ' ', s.strip()) \
                  for s in re.split('\s*(?:%s):\s*' % '|'.join(fields), info)][1:]

        # 將所有資訊填入 item
        movie_item.update(dict(zip(fields, values)))

        yield movie_item
