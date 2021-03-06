import  scrapy
from ..items import AshokLeylandItem
from scrapy.loader import  ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



class AshokLeyland(scrapy.Spider):
    name = "ashok_leyland"
    allowed_domains = ['www.ashokleyland.com']
    start_urls = ["https://www.ashokleyland.com/en/media/press-release/"]

    items = AshokLeylandItem()

    def parse(self, response):
        #self.logger.info('hello this is my first spider')

        for i in range(0,30):
            sel_list = response.xpath('//div[@class="col-md-6 moreNewsWrappers"]')[i]
            loader = ItemLoader(item=AshokLeylandItem(), selector=sel_list)
            loader.add_xpath('links','./a/@href')
            loader.add_xpath('publish_date','./h5/text()')
             # items['links']= sel_list.xpath('./a/@href')[i].get(),
            # items['dates']= sel_list.xpath('./h5/text()')[i].get()
            ashok_leyland_item = loader.load_item()
            link =  sel_list.xpath('./a/@href').get()
            self.logger.info('get article url')
            # go to the author page
            yield response.follow(link,callback=self.parse_author,meta = {'ashok_leyland_item':ashok_leyland_item})


    def parse_author(self, response):
        ashok_leyland_item = response.meta['ashok_leyland_item']
        loader = ItemLoader(item=ashok_leyland_item, response =response)
        sel_list = response.xpath('//div[@class="col-md-8"]/p//text()')
        self.string = ""
        for i in range(0, len(sel_list)):
            text = sel_list[i].get()
            self.string += text + " "

        loader.add_value('text',self.string)

        yield  loader.load_item()


class AshokLeyland_Two(scrapy.Spider):
    name = "ashok_leyland_2"

    def start_requests(self):
        urls = ['https://www.ashokleyland.com/en/media/latest-news', ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('hello this is my first spider')
        for art in response.xpath('//div[@class = "col-md-6 moreNewsWrappers"]'):
            loader = ItemLoader(item=AshokLeylandItem(), selector=art)
            loader.add_xpath('text','./p//text()')
            loader.add_value('links',"")
            loader.add_value('publish_date'," ")
            yield loader.load_item()



settings = get_project_settings()
process = CrawlerProcess(settings=settings)
process.crawl(AshokLeyland)
process.crawl(AshokLeyland_Two)
process.start()