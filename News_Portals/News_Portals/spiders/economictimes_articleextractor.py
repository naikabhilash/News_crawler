# -*- coding: utf-8 -*-
import scrapy

class EconomictimesArticleextractorSpider(scrapy.Spider):
    name = 'economictimes_articleextractor'
    allowed_domains = ['economictimes.indiatimes.com']
    urls = ['https://economictimes.indiatimes.com/industry/','https://economictimes.indiatimes.com/tech/',
    'https://economictimes.indiatimes.com/jobs/','https://economictimes.indiatimes.com/news/company/',
    'https://economictimes.indiatimes.com/markets/stocks/news/',
    'https://economictimes.indiatimes.com/tech/ites/']

    def start_requests(self):
        """
        In this method a request is sent to the mentioned
        url and resonse in generated in the parse method
        """
        for url in self.urls:
            # time.sleep(2)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        links are extracted in this method along with the 
        categories and further requests are sent to the extracted links
        """
        for link in response.xpath('//h2[@class="heading3"]/a'):
            links = link.xpath('./@href').get()
            # time.sleep(0.5)
            yield scrapy.Request(url=links, callback=self.parse_link)
        cat = response.xpath('//div[@class="dtc vam sub-head"]/h1/text()').get()
        for link in response.xpath('//h3/a'):
            links= link.xpath('./@href').get()
            title = link.xpath('.//text()').get()
            # time.sleep(0.5)
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'title':title, 'category':cat})
        for i in range(4,17):
            next_page = 'https://economictimes.indiatimes.com/lazyloadlistnew.cms?msid=2146843&curpg='+str(i)+'&img=0'
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
    def parse_link(self, response):
        """
        links are extracted in this method along with the 
        categories and further requests are sent to the extracted links
        """
        for link in response.xpath('//h2[@class="heading3"]/a'):
            links = link.xpath('./@href').get()
            yield scrapy.Request(url=links, callback=self.parse_article_link)
        cat = response.xpath('//div[@class="dtc vam sub-head"]/h1/text()').get()
        for link in response.xpath('//section[@id="pageContent"]//li/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('.//text()').get()    
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'title':title, 'category':cat})
        for link in response.xpath('//h3/a'):
            links= link.xpath('./@href').get()
            title = link.xpath('.//text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'title':title, 'category':cat})
        
    def parse_article_link(self, response):
        """
        links are extracted in this method along with the 
        categories and further requests are sent to the extracted links
        """
        cat = response.xpath('//div[@class="dtc vam sub-head"]/h1/text()').get()
        for link in response.xpath('//h3/a'):
            links= link.xpath('./@href').get()
            title = link.xpath('.//text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'title':title, 'category':cat})
    
    def parse_article(self, response):
        """
        text of the article and publish dates are
        extracted in this method
        """
        self.title_p = response.request.meta.get('title')
        self.cat_p = response.request.meta.get('category')
        self.link_p = response.request.meta.get('links')
        #sel_list = response.xpath('(// div[@class = "artText medium"])[1]//text()')
        sel_list = response.xpath('(//div[@class="artText"])[1]//text()')
        self.string = ""
        for j in range(0,len(sel_list)):
            text = sel_list[j].get()
            self.string+=text+" "
        publish_date = response.xpath('(//div[@class="dtc vam artByline"]/time/text())[1]').get()
        yield {
        'links' : response.urljoin(self.link_p),
        'title' : self.title_p,
        'text' : self.string,
        'category': self.cat_p,
        'publish_date' : publish_date,
        'company': 'Economic_Times'
        }

    
    

