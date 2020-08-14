# -*- coding: utf-8 -*-
import scrapy

class EconomicAutoExtractorSpider(scrapy.Spider):
    name = 'economic_auto_extractor'
    allowed_domains = ['auto.economictimes.indiatimes.com']
    urls = ['https://auto.economictimes.indiatimes.com/latest-news/',
        'https://auto.economictimes.indiatimes.com/news/auto-technology/','https://auto.economictimes.indiatimes.com/tag/new+launches/']
    
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
        cat = response.xpath('//div[@class="hdngBx"]/h1/text()').get()
        for link in response.xpath('//ul[contains(@class,"lst4 news-listing")]//h3/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for i in self.urls:
            for j in range(2,3):
                next_page = i+str(j)
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
        self.string =""
        sel_list = response.xpath('(//div[@class="Normal"])[1]//text()')
        for i in range(0,len(sel_list)):
            text = sel_list[i].get()
            self.string+=text+" "
        publish_date = response.xpath('//li[@class="date"]/text()').get()
        yield {
        'links' : self.link_p,
        'title' : self.title_p.strip(),
        'text'  : self.string.strip(),
        'category' : self.cat_p.strip(),
        'publish_date' : publish_date,
         'company': 'ET_Auto'
        }


