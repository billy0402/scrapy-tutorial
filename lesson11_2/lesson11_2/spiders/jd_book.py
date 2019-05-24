# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest

from ..items import BookItem

lua_script = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
end
'''


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    base_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&book=y&wq=python'

    def start_requests(self):
        # 請求第一頁，無需 js 繪製
        yield Request(self.base_url, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        # 取得商品總數，計算出總頁數
        total = response.css('span#J_resCount::text').extract_first() \
                        .replace('万+', '')
        total = int(float(total) * 10000)
        page_num = total // 60 + (1 if total % 60 else 0)

        # 建置每頁的 url，向 Splash 的 execute 端點發送請求
        for i in range(page_num):
            url = '{}&page={}'.format(self.base_url, 2 * i + 1)
            yield SplashRequest(url,
                                endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'])

    def parse(self, response):
        # 取得一個頁面中每本書的名字和價格
        book_list = response.css('ul.gl-warp.clearfix > li.gl-item')
        for selector in book_list:
            book = BookItem()

            book['name'] = selector.css('div.p-name').xpath('string(.//em)').extract_first()
            book['price'] = selector.css('div.p-price i::text').extract_first()

            yield book
