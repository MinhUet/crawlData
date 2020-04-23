import scrapy
from ..items import TracuuhoadonItem
class QuoteSpider(scrapy.Spider):
    name = 'tracuuhoadon'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]

    def parse(self, response):

        item = TracuuhoadonItem()

        all_quotes = response.css('div.quote')
        for quotes in all_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()
            item['title'] =  title
            item['author']= author
            item['tag'] = tag
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        print(next_page)
        if next_page is not None:
            yield response.follow