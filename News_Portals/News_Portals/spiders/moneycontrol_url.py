# -*- coding: utf-8 -*-
"""
paid articles will not be scraped
"""
import scrapy

class MoneycontrolUrlSpider(scrapy.Spider):
    name = 'moneycontrol_url'     # name of the spider
    allowed_domains = ['www.moneycontrol.com']   # domain for which spider is built
    urls = ['https://www.moneycontrol.com/news/business/companies/','https://www.moneycontrol.com/news/business/earnings/',
    'https://www.moneycontrol.com/news/tags/auto.html/','https://www.moneycontrol.com/news/india/',
    'https://www.moneycontrol.com/news/business/', 'https://www.moneycontrol.com/news/business/markets/',
    'https://www.moneycontrol.com/news/business/stocks/'] 

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
        cat = response.xpath('//h1[@class="fleft"]/text()').get()
        for link in response.xpath('//h2/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield scrapy.Request(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for j in self.urls:
            for i in range(2,6):
                next_page = j+'page-'+str(i)+'/'
                if next_page:
                    yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        """
        In this method response is taken from all the child links 
        within the parent link and link, text and date is extracted 
        from a particular child link
        """
        self.cat_p = response.request.meta.get('category')
        self.title_p = response.request.meta.get('title')
        self.link_p = response.request.meta['links']
        self.string = ""
        sel_list = response.xpath('(//div[@id="article-main"])[1]//p//text()')
        for j in range(0,len(sel_list)-1):
            text = sel_list[j].get()
            self.string += text + " "
        if self.string == "":
            sel_list = response.xpath('//span[@class="slideshow-caption"]/p//text()')
            for j in range(0,len(sel_list)):
                text = sel_list[j].get()
                self.string += text + " "
        publish_date = response.xpath('//div[@class="arttidate "]/text()').get() 
        yield {
        'links' : self.link_p,
        'title' : self.title_p,
        'text' : self.string,
        'category' : self.cat_p,
        'publish_date' : publish_date,
        'company': 'Moneycontrol'
        }


        

        

        
