# -*- coding: utf-8 -*-
import scrapy

class LivemintArticleextractorSpider(scrapy.Spider):
    name = 'livemint_articleextractor'
    allowed_domains = ['www.livemint.com']
    urls = ['https://www.livemint.com/companies/','https://www.livemint.com/latest-news/',
        'https://www.livemint.com/technology/','https://www.livemint.com/industry/',
        'https://www.livemint.com/industry/infotech/','https://www.livemint.com/companies/news/',
        'https://www.livemint.com/news/india/','https://www.livemint.com/companies/company-results/',
        'https://www.livemint.com/market/']

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
        cat = response.xpath('//h1[@class="listheading"]/text()').get()
        for link in response.xpath('//h1/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for link in response.xpath('//h2/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for i in self.urls:
            for j in range(2,5):
                next_page = i+'page-'+str(j)
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
        self.string=""
        sel_list = response.xpath('(//div[@id="mainArea"])[1]/div[contains(@class, "FirstEle") or contains(@class, "paywall")]/p//text()')
        for j in range(0,len(sel_list)):
            text = sel_list[j].get()
            self.string+=text+" "
        publish_date = response.xpath('((//span[@class="articleInfo pubtime"])[1]//text())[5]').get()
        yield {
        'links' : response.urljoin(self.link_p),
        'title' : self.title_p,
        'text' : self.string,
        'category' : self.cat_p,
        'publish_date' : publish_date,
         'company': 'Live_Mint'
        }

