import scrapy


class ScholarItem(scrapy.Item):
    Author = scrapy.Field()
    Title = scrapy.Field()
    Authors = scrapy.Field()
    Journal = scrapy.Field()
    Year = scrapy.Field()
    Citations = scrapy.Field()
    Total_Citations = scrapy.Field()
    h_index = scrapy.Field()
    i10_index = scrapy.Field()


class Page1Spider(scrapy.Spider):
    name = "Page1"
    page_size = 20
    start = 0
    urls = "https://scholar.google.com/citations?user=uro60HMAAAAJ&hl=en"
    start_urls = [urls + "&cstart={}&pagesize={}".format(start, page_size)]

    def parse(self, response):
        item0 = ScholarItem()
        name = response.css("title::text").get()
        name = str(name)
        if name.endswith("- Google Scholar"):
            name = name[:-16]
        item0["Author"] = Page1Spider.urls + ", " + name
        yield item0

        info_total_citations = response.css("td.gsc_rsb_std::text").extract()[0]
        info_h_index = response.css("td.gsc_rsb_std::text").extract()[2]
        info_i10_index = response.css("td.gsc_rsb_std::text").extract()[3]
        str(info_total_citations)
        str(info_h_index)
        str(info_i10_index)

        item1 = ScholarItem()
        item1["Total_Citations"] = info_total_citations
        item1["h_index"] = info_h_index
        item1["i10_index"] = info_i10_index
        yield item1
        yield scrapy.Request(Page1Spider.urls, callback=self.parse1)

    def parse1(self, response):

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
        yield scrapy.Request(next_page, callback=self.parse1)
