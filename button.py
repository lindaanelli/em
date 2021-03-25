import scrapy


class CitationItem(scrapy.Field):
    Title = scrapy.Field()
    Format = scrapy.Field


class Citation(scrapy.Spider):
    name = "Citation"
    url = "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=10972803237645083033#d=gs_cit&u=%2Fscholar%3Fq%3Dinfo%3ARp0PCiohqMgJ%3Ascholar.google.com%2F%26output%3Dcite%26scirp%3D0%26hl%3Den"
    start_urls = [
        url
    ]

    def parse(self, response):
        # for name in response.css('div#gs_citt'):
        name_title = response.css("div.gs_citr::text").extract()
        name_format = response.css("th.gs_cith::text").extract()

        item = CitationItem()
        item["Title"] = name_title
        item["Format"] = name_format
        yield item
