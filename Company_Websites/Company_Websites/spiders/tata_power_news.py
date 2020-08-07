# -*- coding: utf-8 -*-
import scrapy


class TataPowerNewsSpider(scrapy.Spider):
    name = 'tata_power_news'
    allowed_domains = ['www.tatapower.com']
    urls = ['https://www.tatapower.com/media/media-releases.aspx?utm_medium=301&utm_source=direct&utm_campaign=/media/media-releases.aspx#']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//div[@class="cont-search-results"]//li/a'):
            links = link.xpath('./@href').get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links})
    
    def parse_article(self, response):
        self.link_p = response.request.meta.get('links')
        sel_list = response.xpath('(//div[@class="mrd_Collumn"])[1]/p//text()')
        self.string = ""
        for i in range(0,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "
        sel_date_list = response.xpath('//div[@class="heading"]/span[@class="heading-date"]//text()')
        self.date = ""
        if self.string == "":
            sel_list_n = response.xpath('//div[@class="media-releases-details-container"]/p//text()')
            for j in range(0,len(sel_list_n)):
                text = sel_list_n[j].get()
                self.string += text + " "
        for j in range(0,len(sel_date_list)):
            dates = sel_date_list[j].get()
            self.date += dates + " "
        yield {
        'links': response.urljoin(self.link_p),
        'text' : self.string,
        'publish_date' : self.date.strip()
        }

    
