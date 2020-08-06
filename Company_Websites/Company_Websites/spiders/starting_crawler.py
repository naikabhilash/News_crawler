#scrapy

#-----------------------------
#----https://stackoverflow.com/questions/45309220/scrapy-crawl-multiple-spiders-sharing-same-items-pipeline-and-settings-but-wi
#----https://stackoverflow.com/questions/55894338/make-scrapy-export-to-csv
#-----------------------------
#
# from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.company_websites_spider import AshokLeyland
# from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.company_websites_spider import AshokLeyland_Two
#
# from twisted.internet import reactor
#
# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
#
# settings = get_project_settings()
# settings.set('FEED_FORMAT', 'json')
# settings.set('FEED_URI', 'result.json')
#
# configure_logging()
# runner = CrawlerRunner(settings)
#
# def run():
#
#     runner.crawl(AshokLeyland_Two)
#     runner.crawl(AshokLeyland)
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#
#     reactor.run()  # the script will block here until all crawling jobs are finished
#
# if __name__ == '__main__':
#     run()
#----------------------------------------------
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
# #
# # #spiders
from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.company_websites_spider import AshokLeyland
from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.company_websites_spider import AshokLeyland_Two
from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.adani_news_extract import AdaniNewsExtractSpider
from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.itc_limited_news import ItcLimitedNewsSpider
from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.itc_limited_news import ItcLimitedNewsSpider_Two
from Company_websites_01.Version02.Company_Websites.Company_Websites.spiders.larsentoubro import Larsentoubro
# # from web_crawler.spiders.spider1 import Spider1
# # from web_crawler.spiders.spider2 import Spider2
# #
configure_logging()
settings = get_project_settings()
settings.set('FEED_FORMAT', 'csv')
settings.set('FEED_URI', 'results.csv')
runner = CrawlerRunner(settings)
# #
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(AshokLeyland)
    yield runner.crawl(AshokLeyland_Two)
    yield runner.crawl(AdaniNewsExtractSpider)
    yield runner.crawl(ItcLimitedNewsSpider)
    yield runner.crawl(ItcLimitedNewsSpider_Two)
    yield runner.crawl(Larsentoubro)

    reactor.stop()

if __name__ == '__main__':
    crawl()
    reactor.run()
# #----------------------------------------------

