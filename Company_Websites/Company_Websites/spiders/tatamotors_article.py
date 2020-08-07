# -*- coding: utf-8 -*-
import scrapy
from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader

class TatamotorsArticleSpider(scrapy.Spider):
    name = 'tatamotors_article'
    allowed_domains = ['www.tatamotors.com']
    urls = ['https://www.tatamotors.com/media/press-releases/']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//div[@class="right_sec"]/h3/a'):
            links = link.xpath('./@href').get()
            yield scrapy.Request(url=links, callback=self.parse_article, meta={'links':links})
    
    def parse_article(self, response):
        self.link_p = response.request.meta.get('links')
        sel_list = response.xpath('//div[@id="flowtingHeight"]/p//text()')
        self.string = ""
        for i in range(1,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "
        publish_date = response.xpath('//p[@class="date"]/text()').get()

        loader = ItemLoader(item=CompanyWebsitesItem())
        loader.add_value('links', self.link_p)
        loader.add_value('text', self.string)
        loader.add_value('publish_date', publish_date)
        loader.add_value('company', 'TataMotors')
        yield loader.load_item()



        
