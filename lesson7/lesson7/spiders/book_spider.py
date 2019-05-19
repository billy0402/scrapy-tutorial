import scrapy
from scrapy.linkextractors import LinkExtractor

from ..items import BookItem


class BooksSpider(scrapy.Spider):
    name = 'books'

    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for selector in response.css('article.product_pod'):
            book = BookItem()
            book['name'] = selector.xpath('./h3/a/@title').extract_first()
            book['price'] = selector.css('p.price_color::text').extract_first()

            yield book

        le = LinkExtractor(restrict_css='ul.pager li.next')
        links = le.extract_links(response)

        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)
