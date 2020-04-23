import scrapy
from scrapy.http import FormRequest
# from ..items import TracuuhoadonItem

class TchdSpider(scrapy.Spider):
    name = 'tracuuhoadon'
    start_urls = [
        'http://tracuuhoadon.gdt.gov.vn/tbphtc.html'
    ]



    def parse(self, response):
        tokens = response.css('input::attr(value)').extract()
        token = tokens[-3]
        return FormRequest.from_response(response, formdata={
            'token' : token,
            'mst'   : '0101243150',
            'captcha': '',
            'tungay': '01/01/2017',
            'denngay': '01/01/2020'

        }, callnack=crawldata)

        crawldata():
            return

