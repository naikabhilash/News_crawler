# -*- coding: utf-8 -*-
import scrapy

class InfosysNewsSpider(scrapy.Spider):
    name = 'infosys_news'
    allowed_domains = ['www.infosys.com']
    urls = ['https://www.infosys.com/newsroom/press-releases.html']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        sel_list = response.xpath('//div[@class="col-md-12 col-sm-12 col-xs-12 relative-off lng-txt"]')
        for i in range(0,30):
            links = sel_list.xpath('.//h3/a/@href')[i].get()
            date = sel_list.xpath('//li[@class="lct-txt press-release-date"]/text()')[i].get()
            yield response.follow(url=links, callback=self.parse_article, meta={'links':links, 'date':date})
        
    def parse_article(self, response):
        self.date_p = response.request.meta.get('date')
        self.link_p = response.request.meta.get('links')
        self.string = ""
        sel_list = response.xpath('//div[@class="row"]//p//text()')
        for i in range(0,len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "
        # publish_date = response.xpath('//p[@class="location-date"]/text()').get()
        # if publish_date is None:
        #     publish_date = response.xpath('//p/strong/text()').get()
        yield {
        'links' : response.urljoin(self.link_p),
        'text' : self.string,
        'publish_date' : self.date_p
        }

