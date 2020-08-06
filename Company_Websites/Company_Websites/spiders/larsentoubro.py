# links = response.xpath('//div[@class="contentText"]')
# data = link.xpath('//span[@class="date"]/text()').get()
# href = link.xpath('h3/a/@href').get()
# text = link.xpath('h3/a[@class = "linkText"]/text()').get()

import  scrapy

from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader


class Larsentoubro(scrapy.Spider):
    name = "larsentoubro"

    items = CompanyWebsitesItem()

    def start_requests(self):
        urls = ['https://www.larsentoubro.com/corporate/media/press-releases/',
                'https://www.larsentoubro.com/corporate/media/news/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for i in range(0,39):

            sel_list = response.xpath('//div[@class="contentText"]')[i]
            self.logger.info('get article url - larsentoubro')
            loader = ItemLoader(item=CompanyWebsitesItem(), selector=sel_list)
            loader.add_xpath('text','h3/a[@class = "linkText"]/text()')
            loader.add_xpath('links','h3/a/@href')
            date = sel_list.xpath('//span[@class="date"]/text()')[i].get()
            loader.add_value('publish_date',date)
            loader.add_value('company', 'larsentoubro')
            yield loader.load_item()
