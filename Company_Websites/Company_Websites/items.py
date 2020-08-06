# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class CompanyWebsitesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    links = Field()
    text = Field()
    publish_date = Field()
    company = Field()
    pass
