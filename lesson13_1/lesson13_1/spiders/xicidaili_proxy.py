# -*- coding: utf-8 -*-
import scrapy


class XicidailiProxySpider(scrapy.Spider):
    name = 'xicidaili_proxy'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        pass
