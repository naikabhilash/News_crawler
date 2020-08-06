# -*- coding: utf-8 -*-
import scrapy
from ..items import CompanyWebsitesItem
from scrapy.loader import  ItemLoader

class AdaniNewsExtractSpider(scrapy.Spider):
    name = 'adani_news_extract'
    allowed_domains = ['www.adanienterprises.com']
    urls = ['https://www.adanienterprises.com/newsroom/media-releases/']
    items = CompanyWebsitesItem()

    def start_requests(self):
        """
        this method is used for iterating the list of websites 
        url sending the request and getting the response in parse method
        """
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        this method is used for getting the links of a particular link
        and pagination of the parent link is also taken care of in this 
        method
        """
        for link in response.xpath('//div[@class="col-md-11"]'):
            loader = ItemLoader(item=CompanyWebsitesItem(), selector=link)
            loader.add_xpath('links','./h3/a/@href')
            loader.add_xpath('publish_date','./p/span/text()')
            loader.add_value('company','Adani')
            adani_items = loader.load_item()
            link = link.xpath('./h3/a/@href').get()
            self.logger.info('get article url - adani')

            yield response.follow(url=link, callback=self.parse_article, meta={'adani_items':adani_items})

    def parse_article(self, response):
        """
        In this method response is taken from all the child links 
        within the parent link  and date is extracted 
        from a particular child link and dictionary is created 
        with links, article content and its publish date
        """
        adani_items = response.meta['adani_items']
        loader = ItemLoader(item=adani_items, response=response)
        sel_list = response.xpath('//div[@class="container"]/div[@class="innerPgConten"]//text()')
        self.strng = ""

        for i in range(4,len(sel_list)):
            text = sel_list[i].get()
            self.strng += text + " "

        loader.add_value('text',self.strng)

        yield loader.load_item()



