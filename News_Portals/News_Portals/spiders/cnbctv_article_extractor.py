# -*- coding: utf-8 -*-
import scrapy

class CnbctvArticleExtractorSpider(scrapy.Spider):
    name = 'cnbctv_article_extractor' #name of the spider
    allowed_domains = ['www.cnbctv18.com'] #allowed domain for this spider
    urls = ['https://www.cnbctv18.com/information-technology/',
        'https://www.cnbctv18.com/technology/','https://www.cnbctv18.com/auto/',
        'https://www.cnbctv18.com/earnings/','https://www.cnbctv18.com/energy/',
        'https://www.cnbctv18.com/business/']

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
        link = response.xpath('//section[@class="market_news world_news"]/a/@href').get()
        yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):
        """
        this method follows the parent links and pass the response to 
        the parse_article method
        """
        cat = response.xpath('//div[@class="h1-tilte-wrap MB30"]/h1/text()').get()
        for links in response.xpath('//div[@class="list_title"]/a'):
            link = links.xpath('./@href').get()
            title = links.xpath('./text()').get()
            yield response.follow(url=link, callback=self.parse_article, meta={'links':link, 'category':cat, 'title':title})
        for ur in self.urls:
            for i in range(2,4):
                next_page = ur+'page-'+str(i)+'/'
                if next_page:
                    yield scrapy.Request(url=next_page, callback=self.parse_link)

    def parse_article(self, response):
        """
        In this method response is taken from all the child links 
        within the parent link and link, text and date is extracted 
        from a particular child link
        """
        self.category = response.request.meta.get('category')
        self.title_p = response.request.meta.get('title')
        self.link_p = response.request.meta['links']
        self.string =""
        sel_list = response.xpath('//div[@class="arti-right"]//p//text()')
        for j in range(0,len(sel_list)):
            text = sel_list[j].get()
            self.string += text 
            extra_text = response.xpath('(//div[@class="arti-right"]/aside[@class="details"]/text())[2]').get()
            self.string+=extra_text
        if self.string == "":
            sel_list_1 = response.xpath('//div[@class="vdo_body"]//text()')
            for i in range(0,len(sel_list_1)):
                text = sel_list_1[i].get()
                self.string += text      
        publish_date = response.xpath('(//div[@class="time_stamp"]/text())[2]').get()
        yield {
        'links': self.link_p,
        'title' : self.title_p,
        'text' : self.string,
        'category' : self.category,
        'publish_date' :  publish_date,
         'company': 'CNBCTV18'

        }


