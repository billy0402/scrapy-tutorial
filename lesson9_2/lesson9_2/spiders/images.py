# -*- coding: utf-8 -*-
import scrapy


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def parse(self, response):
        pass
