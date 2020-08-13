# -*- coding: utf-8 -*-
import scrapy
from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader


class TataSteelNewsSpider(scrapy.Spider):
    name = 'tata_steel_news'
    allowed_domains = ['www.tatasteel.com']
    urls = ['https://www.tatasteel.com/media/newsroom/press-releases/']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sel_list = response.xpath('//div[@class="card"]/a')
        for i in range(0,30):
            links = sel_list[i].xpath('./@href').get()
            date = sel_list[i].xpath('./span[@class="date-day"]/span[2]/text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'date':date})
            self.logger.info('get article url - Tata_Steel')

    def parse_article(self, response):
        self.link_p = response.request.meta.get('links')
        self.date_p = response.request.meta.get('date')
        self.string = ""
        sel_list = response.xpath('//div[@class="container prdetails"]/p//text()')
        for i in range(0,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "

        loader = ItemLoader(item=CompanyWebsitesItem())
        loader.add_value('links', response.urljoin(self.link_p))
        loader.add_value('text', self.string.strip())
        loader.add_value('publish_date', self.date_p)
        loader.add_value('company', 'Maruti_Suzuki')
        yield loader.load_item()
