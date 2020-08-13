# -*- coding: utf-8 -*-
import scrapy
from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader

class HclTechNewsSpider(scrapy.Spider):
    name = 'hcl_tech_news'
    allowed_domains = ['www.hcltech.com']
    urls = ['https://www.hcltech.com/media/newsfeed/','https://www.hcltech.com/media/press_release/']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        for link in response.xpath('//td[@class="views-field views-field-title"]//a'):
            links = link.xpath('./@href').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links})
    
    def parse_article(self, response):
        self.link_p = response.request.meta.get('links')
        self.string = ""
        sel_list = response.xpath('//div[@class="news-body"]/p//text()')
        for i in range(0,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "
        publish_date = response.xpath('(//div[@class="news-published-date"]//text())[3]').get()

        loader = ItemLoader(item=CompanyWebsitesItem())
        loader.add_value('links', response.urljoin(self.link_p))
        loader.add_value('text', self.string.strip())
        loader.add_value('publish_date', publish_date)
        loader.add_value('company', 'HCL_Tech')
        yield loader.load_item()

