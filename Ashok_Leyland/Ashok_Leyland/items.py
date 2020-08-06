# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class AshokLeylandItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    links = Field()
    text = Field()
    publish_date = Field()
    pass
