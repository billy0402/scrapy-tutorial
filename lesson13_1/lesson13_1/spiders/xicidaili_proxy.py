# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request


class XicidailiProxySpider(scrapy.Spider):
    name = 'xicidaili_proxy'
    allowed_domains = ['www.xicidaili.com']

    def start_requests(self):
        # 爬取國內高匿代理 http://www.xicidaili.com/nn/ 前三頁
        for i in range(1, 4):
            yield Request('http://www.xicidaili.com/nn/{}'.format(i))

    def parse(self, response):
        for selector in response.xpath('//table[@id="ip_list"]/tr[position()>1]'):
            # 分析代理的 IP.Port.scheme(http or https)
            ip = selector.css('td:nth-child(2)::text').extract_first()
            port = selector.css('td:nth-child(3)::text').extract_first()
            scheme = selector.css('td:nth-child(6)::text').extract_first().lower()

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
