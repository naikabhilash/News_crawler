# -*- coding: utf-8 -*-
import scrapy

class FinancialExtractUrlSpider(scrapy.Spider):
    name = 'financial_extract_url'
    allowed_domains = ['www.financialexpress.com']
    urls = ['https://www.financialexpress.com/industry/technology/',
        'https://www.financialexpress.com/brandwagon/','https://www.financialexpress.com/jobs/',
        'https://www.financialexpress.com/industry/','https://www.financialexpress.com/auto/industry/',
        'https://www.financialexpress.com/market/','https://www.financialexpress.com/lifestyle/science/',
        'https://www.financialexpress.com/india-news/','https://www.financialexpress.com/auto/car-news/',
        'https://www.financialexpress.com/auto/bike-news/','https://www.financialexpress.com/auto/motor-sports/']
   
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
        cat = response.xpath('//h1[contains(@class,"head")]/text()').get()
        for link in response.xpath('//h2/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield scrapy.Request(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for link in response.xpath('//h3/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield scrapy.Request(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for i in self.urls:
            for j in range(2,4):
                next_page = i+'page/'+str(j)+'/'
                if next_page:
                    yield scrapy.Request(url=next_page, callback=self.parse)
    def parse_article(self , response):
        """
        In this method response is taken from all the child links 
        within the parent link  and date is extracted 
        from a particular child link and dictionary is created 
        with links, article content and its publish date
        """
        self.cat_p = response.request.meta.get('category')
        self.title_p = response.request.meta.get('title')
        self.link_p = response.request.meta['links']
        publish_date = response.xpath('//span[@itemprop="dateModified"]/text()').get()
        self.string = ""
        lst_sel = response.xpath('//div[@class="post-summary"]//p//text()')
        for j in range(0,len(lst_sel)):
            text = lst_sel[j].get()
            self.string += text+" "
        lst_sel = response.xpath('//p//text()')
        if self.string == "":
            for j in range(0,len(lst_sel)):
                text = lst_sel[j].get()
                self.string += text+" "
        yield {
        'links' : self.link_p,
        'title' : self.title_p.strip(),
        'text'  : self.string.strip(),
        'category' : self.cat_p.strip(),
        'publish_date' : publish_date,
         'company': 'Financial_Express'
        }




