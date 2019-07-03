# -*- coding: utf-8 -*-
import scrapy


class TestRandomProxySpider(scrapy.Spider):
    name = 'test_random_proxy'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/']

    def parse(self, response):
        pass
