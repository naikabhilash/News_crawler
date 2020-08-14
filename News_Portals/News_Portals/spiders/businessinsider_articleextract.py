# -*- coding: utf-8 -*-
import scrapy


class BusinessinsiderArticleextractSpider(scrapy.Spider):
    name = 'businessinsider_articleextract' # spider name
    allowed_domains = ['www.businessinsider.in'] #allowed domains
    urls = ['https://www.businessinsider.in/tech/',
    'https://www.businessinsider.in/business/','https://www.businessinsider.in/business/corporates/',
    'https://www.businessinsider.in/business/auto/','https://www.businessinsider.in/business/news/',
    'https://www.businessinsider.in/business/corporates/news/','https://www.businessinsider.in/education/']

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
        cat = response.xpath('//div[@class="left_content clearfix"]/h1/text()').get()
        for link in response.xpath('//span[@class="toplist_heading"]/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield scrapy.Request(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for link in response.xpath('//span[@class="liststories_heading"]/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./text()').get()
            yield scrapy.Request(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        for i in self.urls:
            for j in range(2,5):
                next_page = i+str(j)
                if next_page:
                    yield scrapy.Request(url=next_page, callback=self.parse)
    
    def parse_article(self, response):
        """
        In this method response is taken from all the child links 
        within the parent link  and date is extracted 
        from a particular child link and dictionary is created 
        with links, article content and its publish date
        """
        self.title = response.request.meta.get('title')
        self.category = response.request.meta.get('category')
        self.link_p = response.request.meta['links']
        self.string = ""
        lst_sel = response.xpath('(//div[@class="Normal"])[1]//text()')
        for j in range(0,len(lst_sel)):
            text = lst_sel[j].get()
            self.string += text+ " "
        if self.string == "":
            lst_sel = response.xpath('(//div[@class="slidelist_more"])[1]//p//text()')
            for j in range(0,len(lst_sel)):
                text = lst_sel[j].get()
                self.string += text+ " "
        publish_date = response.xpath('(//span[@class="Date"])[1]/text()').get()
        yield {
        'links' : self.link_p,
        'title' : self.title,
        'text' : self.string,
        'category' : self.category,
        'publish_date' : publish_date,
         'company' : 'Business_Insider'
        }


