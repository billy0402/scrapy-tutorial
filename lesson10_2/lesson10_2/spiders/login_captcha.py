# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request, FormRequest
from PIL import Image
from io import BytesIO
import pytesseract
from scrapy.log import logger


class LoginCaptchaSpider(scrapy.Spider):
    name = 'login_captcha'
    allowed_domains = ['books.com.tw']
    start_urls = ['http://books.com.tw/']

    def parse(self, response):
        pass

    # -------------------------------------------------- 登入 --------------------------------------------------
    # 登入頁面的 url
    login_url = 'https://cart.books.com.tw/member/login'
    login_id = 'your_login_id'
    password = 'your_password'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        login_response = response.meta.get('login_response')

        if not login_response:
            # 此時，response為登入頁面的回應，從中分析驗證碼圖片的 url，下載驗證碼圖片
            captcha_url = response.css('div#captcha_img img::attr(src)').extract_first()
            captcha_url = response.urljoin(captcha_url)

            # 建置 Request 時，將目前 response 儲存到 meta 字典中
            yield Request(captcha_url,
                          callback=self.login,
                          meta={'login_response': response},
                          dont_filter=True)

        else:
            # 此時，response為驗證碼圖片的回應，response.body 是圖片二進位資料
            # login_response 為登入頁面的回應，用其建置表單請求並發送
            form_data = {
                'login_id': self.login_id,
                'password': self.password,
                'code': self.get_captcha_by_user(response.body),
            }

            yield FormRequest.from_response(login_response,
                                            callback=self.parse_login,
                                            formdata=form_data,
                                            dont_filter=True)

    def parse_login(self, response):
        # 根據回應結果判斷是否登入成功
        info = json.loads(response.text)
        if info['error'] == '0':
            logger.info('登入成功 :)')
            return super().start_requests()

        logger.info('登入失敗，請重新登入 :(')
        return self.start_requests()

    def get_captcha_by_ocr(self, data):
        # OCR 辨識
        image = Image.open(BytesIO(data))
        image = image.convert('L')
        captcha = pytesseract.image_to_string(image)
        image.close()

        return captcha

    def get_captcha_by_network(self, data):
        # 平台辨識
        import requests
        import base64

        url = 'http://ali-checkcode.showapi.com/checkcode'
        appcode = 'f239ccawf37f287418a90e2f922649273c4'

        form = {}
        form['convert_to_jpg'] = '0'
        form['img_base64'] = base64.b64encode(data)
        form['typeId'] = '3040'

        headers = {'Authorization': 'APPCODE ' + appcode}
        response = requests.post(url, headers=headers, data=form)
        res_json = response.json()

        if res_json['showapi_res_code'] == 0:
            return res_json['showapi_res_body']['Result']

        return ''

    def get_captcha_by_user(self, data):
        # 人工識別
        image = Image.open(BytesIO(data))
        image.show()
        captcha = input('請輸入驗證碼: ')
        image.close()

        return captcha
