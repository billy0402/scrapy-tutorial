# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile']

    def parse(self, response):
        # 解析登入後下載的頁面，此例中為使用者個人資訊頁面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()

        yield dict(zip(keys, values))

    # -------------------------------------------------- 登入 --------------------------------------------------
    # 登入頁面的 url
    login_url = 'http://example.webscraping.com/places/default/user/login'
    email = 'liushuo@webscraping.com'
    password = '12345678'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        # 先分析3個隱藏 <input> 中包含的資訊，它們在 <div style="display:none;"> 中
        # selector = response.xpath('//div[@style]/input')
        # 建置表單數據字典
        # form_data = dict(zip(selector.xpath('./@name').extract(), selector.xpath('./@value').extract()))
        # 填寫帳號密碼
        # form_data['email'] = self.email
        # form_data['password'] = self.password
        # yield FormRequest(self.login_url, formdata=form_data, callback=self.parse_login)

        # 登入頁面的解析函數，建置 FormRequest 物件 傳送表單
        form_data = {'email': self.email, 'password': self.password}
        yield FormRequest.from_response(response, formdata=form_data, callback=self.parse_login)

    def parse_login(self, response):
        # 登入成功後，繼續爬取 start_urls 中的頁面
        if 'Welcome Liu' in response.text:
            yield from super().start_requests()
