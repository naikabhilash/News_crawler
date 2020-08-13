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
#from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

# #
# # #spiders
from Company_Websites.Company_Websites.spiders.company_websites_spider import AshokLeyland
#No need to use AshokLeyland_Two as the output is without any date
#from Company_Websites.Company_Websites.spiders.company_websites_spider import AshokLeyland_Two
from Company_Websites.Company_Websites.spiders.adani_news_extract import AdaniNewsExtractSpider
from Company_Websites.Company_Websites.spiders.itc_limited_news import ItcLimitedNewsSpider
from Company_Websites.Company_Websites.spiders.itc_limited_news import ItcLimitedNewsSpider_Two
from Company_Websites.Company_Websites.spiders.larsentoubro import Larsentoubro
from Company_Websites.Company_Websites.spiders.tcs_news_extract import TcsNewsExtractSpider
from Company_Websites.Company_Websites.spiders.tatamotors_article import TatamotorsArticleSpider
from Company_Websites.Company_Websites.spiders.mahindra_mahindra_news import MahindraMahindraNewsSpider
from Company_Websites.Company_Websites.spiders.maruti_suzuki_news import MarutiSuzukiNewsSpider
from Company_Websites.Company_Websites.spiders.hcl_tech_news import HclTechNewsSpider
from Company_Websites.Company_Websites.spiders.infosys_news import InfosysNewsSpider
from Company_Websites.Company_Websites.spiders.tata_steel_news import TataSteelNewsSpider
from Company_Websites.Company_Websites.spiders.tata_power_news import TataPowerNewsSpider



configure_logging()

settings= Settings()
settings.set('FEED_FORMAT', 'csv')
settings.set('FEED_URI', 'results.csv')
runner = CrawlerRunner(settings)
#
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(AshokLeyland)
    #yield runner.crawl(AshokLeyland_Two)
    yield runner.crawl(AdaniNewsExtractSpider)
    yield runner.crawl(ItcLimitedNewsSpider)
    yield runner.crawl(ItcLimitedNewsSpider_Two)
    yield runner.crawl(Larsentoubro)
    yield runner.crawl(TcsNewsExtractSpider)
    yield runner.crawl(TatamotorsArticleSpider)
    yield runner.crawl(MahindraMahindraNewsSpider)
    yield runner.crawl(MarutiSuzukiNewsSpider)
    yield runner.crawl(HclTechNewsSpider)
    yield runner.crawl(InfosysNewsSpider)
    yield runner.crawl(TataSteelNewsSpider)
    yield runner.crawl(TataPowerNewsSpider)

    reactor.stop()

if __name__ == '__main__':
    crawl()
    reactor.run()
# #----------------------------------------------

