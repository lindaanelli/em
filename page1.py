"""
a. il codice funziona, riesce a scrapare tutti i campi -> unico problema: si "interrompe" con un errore (dopo aver
acquisito correttamente ogni campo)
"""

import scrapy


class ScholarItem(scrapy.Item):
    Title = scrapy.Field()
    Authors = scrapy.Field()
    Journal = scrapy.Field()
    Year = scrapy.Field()
    Citations = scrapy.Field()


class Page1Spider(scrapy.Spider):
    name = "Page1"
    page_size = 20
    start = 0
    urls = "https://scholar.google.it/citations?user=utmt89wAAAAJ&hl=it"
    start_urls = [urls + "&cstart={}&pagesize={}".format(start, page_size)]

    def parse(self, response):
        for paper in response.css("tr.gsc_a_tr"):

            paper_title = paper.css("a::text").extract_first()
            paper_authors = paper.css("div.gs_gray::text").extract()[0]
            try:
                paper_journal = paper.css("div.gs_gray::text").extract()[1]
            except IndexError:
                paper_journal = "-"
            paper_year = paper.css("span.gsc_a_h.gsc_a_hc.gs_ibl::text").get()
            paper_ncit = paper.css("a.gsc_a_ac.gs_ibl::text").extract()
            if not paper_ncit:
                paper_ncit = 0

            item = ScholarItem()
            item['Title'] = paper_title
            item['Authors'] = paper_authors
            item['Journal'] = paper_journal
            item['Year'] = paper_year
            item['Citations'] = paper_ncit
            yield item

        Page1Spider.start += Page1Spider.page_size
        next_page = Page1Spider.start_urls[0] + "&cstart={}&pagesize={}".format(Page1Spider.start, Page1Spider.page_size)
        yield scrapy.Request(next_page, callback=self.parse)
