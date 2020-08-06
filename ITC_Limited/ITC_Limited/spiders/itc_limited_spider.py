import  scrapy
from .. items import ItcLimitedItem
from scrapy.loader import ItemLoader

class itc_spider(scrapy.Spider):
    name = 'itc_limited'
    allowed_domains = ['www.itcportal.com']
    start_urls = ['https://www.itcportal.com/media-centre/press-releases.aspx',
            'https://www.itcportal.com/media-centre/press-reports.aspx']

    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        article_items =ItcLimitedItem()

        all_div_articles = response.xpath('//div[@class="press-list"]/ul/li')

        for article in all_div_articles:
            # loader = ItemLoader(item=ItcLimitedItem() ,selector=article)
            # loader.add_xpath('url','./h4/a/@href')
            # loader.add_xpath('published_date','./span/em/text()')
            # article_item  = loader.load_item()
            # text_url = article.css('.press-list>ul>li>h4>a::attr(href)').get()
            # yield response.follow(text_url,self.parse_texturl,meta={'article_item': article_item}
            url = article.xpath('./h4/a/@href').extract()
            published_date = article.xpath('./span/em/text()').extract() + \
                                article.xpath('./span/text()').extract()
            text_url = article.css('.press-list>ul>li>h4>a::attr(href)').get()


            article_items['url'] = url
            article_items['published_date'] = published_date

            yield response.follow(text_url,self.parse_texturl,meta={'article_items': article_items})

    def parse_texturl(self,response):
        article_items = response.meta['article_items']
        loader = ItemLoader(item=article_items, response=response)
        loader.add_xpath('text','//div[@class="press-list-det"]//text()[1]')
        yield loader.load_item()