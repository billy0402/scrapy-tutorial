# -*- coding: utf-8 -*-
import scrapy


class LoginCaptchaSpider(scrapy.Spider):
    name = 'login_captcha'
    allowed_domains = ['books.com.tw']
    start_urls = ['http://books.com.tw/']

    def parse(self, response):
        pass
