import scrapy
from ..get_bibtex_link import Bibtex
from ..items import MainItem
from ..items import PublicationItem
from ..items import BibTeXItem


class ScholarSpider(scrapy.Spider):
    name = "scholar_spider"
    page_size = 20
    start = 0
    urls = "https://scholar.google.it/citations?hl=it&user=GlGtfn8AAAAJ"
    start_urls = [urls + "&cstart={}&pagesize={}".format(start, page_size)]
    bib_link = []
    page2_links = []

    def parse(self, response):  # Scraping author's info
        item0 = MainItem()
        name = response.css("title::text").get()
        name = str(name)
        if name.endswith("- Google Scholar"):
            name = name[:-16]
        item0["Author"] = name
        item0["Link"] = ScholarSpider.urls
        yield item0

        info_total_citations = response.css("td.gsc_rsb_std::text").extract()[0]
        info_h_index = response.css("td.gsc_rsb_std::text").extract()[2]
        info_i10_index = response.css("td.gsc_rsb_std::text").extract()[4]
        str(info_total_citations)
        str(info_h_index)
        str(info_i10_index)

        item1 = MainItem()
        item1["Total_Citations"] = info_total_citations
        item1["h_index"] = info_h_index
        item1["i10_index"] = info_i10_index
        yield item1
        yield scrapy.Request(ScholarSpider.urls, callback=self.parse1)

    def parse1(self, response): # Scraping publication info

        for paper in response.css("tr.gsc_a_tr"):

            paper_title = paper.css("a::text").extract_first()
            try:
                paper_authors = paper.css("div.gs_gray::text").extract()[0]
            except IndexError: # When an index error occurs it means that the web page has no more papers. It's time to scrape BibTeX

                page2_clean = [string for string in ScholarSpider.page2_links if string != ""]
                bib_link_total = []

                for citation in page2_clean:
                    bib = Bibtex(citation)
                    ScholarSpider.bib_link = bib.cit()
                    bib_link_total.append(ScholarSpider.bib_link)

                for lin in bib_link_total:
                    for url in lin:
                        yield scrapy.Request(url, callback=self.parse3)
            try:
                paper_journal = paper.css("div.gs_gray::text").extract()[1]
            except IndexError:
                paper_journal = "-"
            paper_year = paper.css("span.gsc_a_h.gsc_a_hc.gs_ibl::text").get()
            paper_ncit = paper.css("a.gsc_a_ac.gs_ibl::text").extract()
            if not paper_ncit:
                paper_ncit = [0]
            ref = paper.css("td.gsc_a_c a.gsc_a_ac.gs_ibl::attr(href)").get()
            ScholarSpider.page2_links.append(str(ref))

            item = PublicationItem()
            item['Title'] = paper_title
            item['Authors'] = paper_authors
            item['Journal'] = paper_journal
            item['Year'] = paper_year
            item['N_Citations'] = paper_ncit[0]
            yield item

        ScholarSpider.start += ScholarSpider.page_size
        next_page = ScholarSpider.start_urls[0] + "&cstart={}&pagesize={}".format(ScholarSpider.start,
                                                                                  ScholarSpider.page_size)
        yield scrapy.Request(next_page, callback=self.parse1)

    def parse3(self, response):
        item = BibTeXItem()
        item["Type"] = response.text
        yield item
