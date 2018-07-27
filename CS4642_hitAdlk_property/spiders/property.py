# -*- coding: utf-8 -*-
import scrapy


class PropertySpider(scrapy.Spider):
    name = 'property'

    def start_requests(self):
        urls = [
            'http://www.hitad.lk/EN/property?page=0',
        ]
        for i in range(1, 579):
            urls.append('http://www.hitad.lk/EN/property?page=' + str(i * 25))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for Property in response.css('ul.cat-ads'):
            link = Property.css('div.clearfix a::attr(href)').extract()[0]
            yield scrapy.Request(url=link, callback=self.parse2)

    def parse2(self, response):
        for line in response.css('div.fw_b'):
            data = line.css('div.col-lg-12::text').extract()
            yield {
                'Published By': data[0],
                'Sale Type': data[1],
                'Sub Category': data[2],
                'property Type': data[3],
            }
