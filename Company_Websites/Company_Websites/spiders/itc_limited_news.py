# -*- coding: utf-8 -*-
import scrapy
from numpy import unicode

from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader


class ItcLimitedNewsSpider(scrapy.Spider):
    name = 'itc_limited_news'
    allowed_domains = ['www.itcportal.com']
    urls = ['https://www.itcportal.com/media-centre/press-releases.aspx']
    items = CompanyWebsitesItem()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//div[@class="press-list"]/ul/li'):
            loader = ItemLoader(item=CompanyWebsitesItem(), selector=link)
            loader.add_xpath('links','./h4/a/@href')
            loader.add_xpath('publish_date','./span/text()')
            loader.add_value('company','itc_limited')
            itc_limited_items = loader.load_item()

            link = link.xpath('./h4/a/@href').get()
            self.logger.info('get article url - itc_limited_01')

            yield response.follow(url=link, callback=self.parse_itc_article, meta={'itc_limited_items':itc_limited_items})
    
    def parse_itc_article(self, response):
        itc_limited_items = response.meta['itc_limited_items']
        loader = ItemLoader(item= itc_limited_items,response=response)

        sel_list = ' '.join(map(unicode.strip,response.xpath('*//div[@class="press-list-det"]//text()').extract())).replace('\xa0','').replace(',','')
        # Response for the article text comes in a list which is needed to be joined so that a paragraph can be formed

        loader.add_value('text',sel_list)

        yield loader.load_item()


class ItcLimitedNewsSpider_Two(scrapy.Spider):
    name = 'itc_limited_news_02'
    allowed_domains = ['www.itcportal.com']
    urls = ['https://www.itcportal.com/media-centre/press-reports.aspx']
    items = CompanyWebsitesItem()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//div[@class="press-list"]/ul/li'):
            loader = ItemLoader(item=CompanyWebsitesItem(), selector=link)
            loader.add_xpath('links', './h4/a/@href')
            loader.add_xpath('publish_date', './span/em/text()')
            loader.add_value('company', 'itc_limited')
            itc_limited_items = loader.load_item()

            link = link.xpath('./h4/a/@href').get()
            self.logger.info('get article url - itc_limited_02')

            yield response.follow(url=link, callback=self.parse_itc_article,
                                  meta={'itc_limited_items': itc_limited_items})

    def parse_itc_article(self, response):
        itc_limited_items = response.meta['itc_limited_items']
        loader = ItemLoader(item=itc_limited_items, response=response)

        sel_list = (response.xpath('//div[@class="press-list-det"]//text()'))
        self.string = ""
        for i in range(0, len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "

        loader.add_value('text', sel_list)

        yield loader.load_item()
