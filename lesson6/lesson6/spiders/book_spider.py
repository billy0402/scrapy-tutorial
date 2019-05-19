import scrapy

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

        next_url = response.css('ul.pager li.next a::attr(href)') \
                           .extract_first()

        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
