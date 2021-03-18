import scrapy


class ScholarItem(scrapy.Item):
    Title = scrapy.Field()
    Authors = scrapy.Field()
    Description = scrapy.Field()


class CitSpider(scrapy.Spider):

    name = "page2"
    domain = 'https://scholar.google.it/scholar?oi=bibs&hl=it'
    cites = '10972803237645083033'
    start_urls = [domain + '&cites={}'.format(cites)]
    pagesize = 10

    def parse(self, response):

        for paper in response.css("div.gs_r.gs_or.gs_scl div.gs_ri"):

            paper_title = paper.css("h3.gs_rt a::text").extract_first()
            paper_authors = paper.css("div.gs_a a::text").extract()
            paper_description = paper.css("div.gs_rs::text").get()

            item = ScholarItem()
            item['Title'] = paper_title
            item['Authors'] = paper_authors
            item['Description'] = paper_description
            yield item
