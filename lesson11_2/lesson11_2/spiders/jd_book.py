# -*- coding: utf-8 -*-
import scrapy


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    start_urls = ['http://search.jd.com/']

    def parse(self, response):
        pass
