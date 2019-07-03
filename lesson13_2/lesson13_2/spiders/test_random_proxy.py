# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request


class TestRandomProxySpider(scrapy.Spider):
    name = 'test_random_proxy'
    allowed_domains = ['httpbin.org']

    def start_requests(self):
        for _ in range(100):
            yield Request('http://httpbin.org/ip', dont_filter=True)
            yield Request('https://httpbin.org/ip', dont_filter=True)

    def parse(self, response):
        print(json.loads(response.text))
