# -*- coding: utf-8 -*-
import scrapy

class ReutersLinkextractSpider(scrapy.Spider):
    name = 'reuters_linkextract'                  #spider name
    allowed_domains = ['in.reuters.com']          #allowed domains for the spider
    urls = ['https://in.reuters.com/finance/markets/companyOutlooksNews/',
        'https://in.reuters.com/news/technology/', 'https://in.reuters.com/news/top-news/',
        'https://in.reuters.com/finance/','https://in.reuters.com/finance/deals/',
        'https://in.reuters.com/subjects/autos/','https://in.reuters.com/news/archive/businessnews/',
        'https://in.reuters.com/energy-environment/']
   
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
        cat = response.xpath('//header[@class="module-header "]/h1/text()').get()
        self.keys = ['top-news','technologynews','gca-earnings','businessnews','indiadeals','autos-upclose','businessnews','environmentnews'] # keyword for urls pagination further processing
        for link in response.xpath('//div[@class="story-content"]/a'):
            links = link.xpath('./@href').get()
            title = link.xpath('./h3[@class="story-title"]/text()').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'category':cat, 'title':title})
        
        for j in self.keys:
            for i in range(1,4):
                next_page = 'https://in.reuters.com/news/archive/'+j+'?view=page&page='+str(i)+'&pageSize=10'
                if next_page:
                    yield scrapy.Request(url=next_page, callback=self.parse)
    def parse_article(self, response):
        """
        In this method response is taken from all the child links 
        within the parent link  and date is extracted 
        from a particular child link and dictionary is created 
        with links, article content and its publish date
        """
        self.cat_p = response.request.meta.get('category')
        self.title_p = response.request.meta.get('title')
        self.link_p = response.request.meta['links']
        self.strng = ""
        for article in response.xpath('//div[@class="StandardArticleBody_body"]//p'):
            text = article.xpath('.//text()').get()
            self.strng += text + " "
        publish_date = response.xpath('//div[@class="ArticleHeader_date"]/text()').get().split(' /',1)[0]

        if self.title_p == "":
            self.title_p = response.xpath('//h1[@class="ArticleHeader_headline"]/text()').get()
        yield {
        'links' : response.urljoin(self.link_p),
        'title' : self.title_p,
        'text'  : self.strng,
        'category' : self.cat_p,
        'publish_date' : publish_date,
        'company' : 'Reuters'
        }

