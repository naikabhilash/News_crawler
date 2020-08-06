# -*- coding: utf-8 -*-
import scrapy
import json

class TcsNewsExtractSpider(scrapy.Spider):
    name = 'tcs_news_extract'
    allowed_domains = ['www.tcs.com']

    def start_requests(self):
        urls = ['https://www.tcs.com/services/tcs/cardsWithFilter?searchIn=/content/tcs&offset=0&limit=10&tagId=tcs:discover-tcs/about-us/news&year=All&month=All&isCSPage=&sortBy=publishedDate',
        'https://www.tcs.com/services/tcs/cardsWithFilter?searchIn=/content/tcs&offset=0&limit=10&tagId=tcs:discover-tcs/about-us/news&year=All&month=All&isCSPage=&sortBy=publishedDate',
        'https://www.tcs.com/services/tcs/cardsWithFilter?searchIn=/content/tcs&offset=0&limit=10&tagId=tcs:discover-tcs/about-us/analyst-report&year=All&month=All&isCSPage=&sortBy=publishedDate']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        data = json.loads(response.body)
        links = data.get('search_result').get('commonSearchResultList')
        for link in links:
            link_path = link.get('pagePath')
            dates = link.get('newsPublishedDate')
            yield scrapy.Request(url=link_path, callback=self.parse_article, meta={'links':link_path, 'dates':dates})

    def parse_article(self, response):
        self.link_p = response.request.meta.get('links')
        self.date_p = response.request.meta.get('dates')
        sel_list = response.xpath('//div[contains(@class,"text-content abstract-text-content")]//p//text()')
        self.string = ""
        for i in range(0,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "
        data ={}
        data['links'] = self.link_p
        data['text'] = self.string
        data['publish_date'] = self.date_p
        yield data
        