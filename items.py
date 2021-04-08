# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EntitymatchingItem(scrapy.Item):
    Author = scrapy.Field()
    Title = scrapy.Field()
    Authors = scrapy.Field()
    Journal = scrapy.Field()
    Year = scrapy.Field()
    Citations = scrapy.Field()
    Total_Citations = scrapy.Field()
    h_index = scrapy.Field()
    i10_index = scrapy.Field()
    pass
