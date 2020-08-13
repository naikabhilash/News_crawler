    # -*- coding: utf-8 -*-
import scrapy
from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader

class MahindraMahindraNewsSpider(scrapy.Spider):
    name = 'mahindra_mahindra_news'
    allowed_domains = ['www.mahindra.com']
    urls = ['https://www.mahindra.com/news-room/news-stories',
            'https://www.mahindra.com/news-room/press-release']

    #'https://www.mahindra.com/news-room/press-release/',
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//div[@class="col-md-4 col-sm-4 news-item"]'):
            links = link.xpath(' .//h4/a/@href').get()
            dates = link.xpath('./p[@class="date"]/text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'dates':dates})
        for link in response.xpath('//div[@class="col-md-4 col-sm-4 news-item last"]'):
            links = link.xpath(' .//h4/a/@href').get()
            dates = link.xpath('./p[@class="date"]/text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'dates':dates})
        for link in response.xpath('//div[@class="col-md-4 col-sm-4 news-item hidden-xs"]'):
            links = link.xpath(' .//h4/a/@href').get()
            dates = link.xpath('./p[@class="date"]/text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links': links, 'dates': dates})
        self.logger.info('get article url - Mahindra')

    def parse_article(self, response):
        self.link_p = response.request.meta.get('links')
        self.date_p = response.request.meta.get('dates')
        sel_list = response.xpath('//div[@class="article-ctnt"]/p//text()')
        self.string = ""
        for i in range(0,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "

        loader = ItemLoader(item=CompanyWebsitesItem())
        loader.add_value('links', response.urljoin(self.link_p))
        loader.add_value('text', self.string)
        loader.add_value('publish_date', self.date_p)
        loader.add_value('company', 'Mahindra')
        yield loader.load_item()

