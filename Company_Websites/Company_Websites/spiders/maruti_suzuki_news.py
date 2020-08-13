# -*- coding: utf-8 -*-
import scrapy
from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader


class MarutiSuzukiNewsSpider(scrapy.Spider):
    name = 'maruti_suzuki_news'
    allowed_domains = ['www.marutisuzuki.com']
    urls = ['https://www.marutisuzuki.com/corporate/media/press-releases/']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sel_list = response.xpath('//div[@class="events-slider rectangle-dots row"]/a')
        for i in range(0,11):
            links = sel_list.xpath('./@href')[i].get()
            dates = sel_list.xpath('.//div[@class="offset-content"]/span/text()')[i].get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'dates':dates})
            self.logger.info('get article url - Maruti_Suzuki')
            
    def parse_article(self, response):
        self.link_p = response.request.meta.get('links')
        self.date_p = response.request.meta.get('dates')
        sel_list = response.xpath('//div[contains(@class,"contenttable")]//text()')
        self.string = ""
        for i in range(4,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "

        loader = ItemLoader(item=CompanyWebsitesItem())
        loader.add_value('links', response.urljoin(self.link_p))
        loader.add_value('text', self.string.strip())
        loader.add_value('publish_date', self.date_p)
        loader.add_value('company', 'Maruti_Suzuki')
        yield loader.load_item()
