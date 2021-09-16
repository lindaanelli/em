# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MainItem(scrapy.Item):
    a_ID = scrapy.Field()
    Author = scrapy.Field()
    Link = scrapy.Field()
    Total_Citations = scrapy.Field()
    h_index = scrapy.Field()
    i10_index = scrapy.Field()
    Publications = scrapy.Field()
    pass


class PublicationItem(scrapy.Item):
    a_ID = scrapy.Field()
    p_ID = scrapy.Field()
    Title = scrapy.Field()
    Authors = scrapy.Field()
    Journal = scrapy.Field()
    Year = scrapy.Field()
    N_Citations = scrapy.Field()
    BibTeX_Cits = scrapy.Field()
    pass


class BibTeXItem(scrapy.Item):
    p_ID = scrapy.Field()
    Type = scrapy.Field()
    Id = scrapy.Field()
    Bib_Title = scrapy.Field()
    Bib_Author = scrapy.Field()
    Bib_Journal = scrapy.Field()
    Volume = scrapy.Field()
    Pages = scrapy.Field()
    Bib_Year = scrapy.Field()
    Publisher = scrapy.Field()
    pass


class CitationItem(scrapy.Item):
    p_ID = scrapy.Field()
    c_ID = scrapy.Field()
    Title = scrapy.Field()
    Author = scrapy.Field()
    Paper = scrapy.Field()
