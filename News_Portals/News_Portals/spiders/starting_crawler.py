
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
#from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

# #
# # #spiders
# from News_Portals.News_Portals.spiders.businessinsider_articleextract import BusinessinsiderArticleextractSpider
# from News_Portals.News_Portals.spiders.reuters_linkextract import ReutersLinkextractSpider
# from News_Portals.News_Portals.spiders.cnbctv_article_extractor import CnbctvArticleExtractorSpider
# from News_Portals.News_Portals.spiders.economic_auto_extractor import EconomicAutoExtractorSpider
# from News_Portals.News_Portals.spiders.economictimes_articleextractor import EconomictimesArticleextractorSpider
from News_Portals.News_Portals.spiders.financial_express import FinancialExtractUrlSpider
from News_Portals.News_Portals.spiders.livemint_articleextractor import LivemintArticleextractorSpider
from News_Portals.News_Portals.spiders.moneycontrol_url import MoneycontrolUrlSpider


configure_logging()

settings= Settings()
settings.set('FEED_FORMAT', 'csv')
settings.set('FEED_URI', 'results.csv')
runner = CrawlerRunner(settings)
#
@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(BusinessinsiderArticleextractSpider)
    # yield runner.crawl(ReutersLinkextractSpider)
    # yield runner.crawl(CnbctvArticleExtractorSpider)
    # yield runner.crawl(EconomicAutoExtractorSpider)
    # yield runner.crawl(EconomictimesArticleextractorSpider)
    yield runner.crawl(FinancialExtractUrlSpider)
    yield runner.crawl(LivemintArticleextractorSpider)
    yield runner.crawl(MoneycontrolUrlSpider)

    reactor.stop()

if __name__ == '__main__':
    crawl()
    reactor.run()
# #----------------------------------------------

