# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request


class FreeProxyListSpider(scrapy.Spider):
    name = 'free_proxy_list'
    allowed_domains = ['free-proxy-list.net']
    start_urls = ['https://free-proxy-list.net/']

    def parse(self, response):
        for selector in response.xpath('//table[@id ="proxylisttable"]/tbody/tr'):
            # 分析代理的 IP.Port.scheme(http or https)
            ip = selector.css('td:nth-child(1)::text').extract_first()
            port = selector.css('td:nth-child(2)::text').extract_first()
            is_https = selector.css('td:nth-child(7)::text').extract_first()
            scheme = 'https' if is_https == 'yes' else 'http'

            # 使用爬取到的代理再次發送請求到 http(s)://httpbin.org/ip 驗證代理是否可用
            url = '{}://httpbin.org/ip'.format(scheme)
            proxy = '{}://{}:{}'.format(scheme, ip, port)

            meta = {
                'proxy': proxy,
                'dont_retry': True,
                'download_timeout': 10,

                # 以下兩個欄位是傳遞給 check_available 方法的資訊，方便檢測
                '_proxy_scheme': scheme,
                '_proxy_ip': ip,
            }

            yield Request(url, callback=self.check_available,
                          meta=meta, dont_filter=True)

    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']
        check_ip = json.loads(response.text)['origin'].split(', ')

        # 判斷代理是否具有隱藏 IP 功能
        if proxy_ip in check_ip:
            yield {
                'proxy_scheme': response.meta['_proxy_scheme'],
                'proxy': response.meta['proxy']
            }
