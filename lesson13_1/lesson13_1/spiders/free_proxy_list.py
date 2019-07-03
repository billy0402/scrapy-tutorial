# -*- coding: utf-8 -*-
import scrapy


class FreeProxyListSpider(scrapy.Spider):
    name = 'free_proxy_list'
    allowed_domains = ['free-proxy-list.net']
    start_urls = ['http://free-proxy-list.net/']

    def parse(self, response):
        pass
