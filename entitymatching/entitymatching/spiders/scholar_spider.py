import scrapy
from ..get_bibtex_link import Bibtex
from ..items import MainItem
from ..items import PublicationItem
from ..items import BibTeXItem
from ..items import CitationItem


class ScholarSpider(scrapy.Spider):
    name = "scholar_spider"
    page_size = 20
    start = 0
    start2 = 10
    urls = "https://scholar.google.it/citations?user=qKNoouoAAAAJ&hl=it"
    a_id = hash(urls)
    start_urls = [urls + "&cstart={}&pagesize={}".format(start, page_size)]
    bib_link = []
    page2_links = []
    hash_list = []
    citation_dict = {}
    go_bibtex = False

    i = 0

    def parse(self, response):  # Scraping author's info
        item0 = MainItem()
        name = response.css("title::text").get()
        name = str(name)
        if name.endswith("- Google Scholar"):
            name = name[:-16]
        item0["Author"] = name
        item0["Link"] = ScholarSpider.urls
        item0["a_ID"] = ScholarSpider.a_id

        info_total_citations = response.css("td.gsc_rsb_std::text").extract()[0]
        info_h_index = response.css("td.gsc_rsb_std::text").extract()[2]
        info_i10_index = response.css("td.gsc_rsb_std::text").extract()[4]
        str(info_total_citations)
        str(info_h_index)
        str(info_i10_index)

        item0["Total_Citations"] = info_total_citations
        item0["h_index"] = info_h_index
        item0["i10_index"] = info_i10_index
        yield item0
        yield scrapy.Request(ScholarSpider.urls, callback=self.parse1)

    def parse1(self, response):  # Scraping publication info

        for paper in response.css("tr.gsc_a_tr"):

            paper_title = paper.css("a::text").extract_first()
            p_ID = hash(paper_title)

            try:
                paper_authors = paper.css("div.gs_gray::text").extract()[0]

            except IndexError:  # When an index error occurs it means that the web page has no more papers.
                # It's time to scrape BibTeX

                if ScholarSpider.go_bibtex:
                    bib_link_total = []
                    for (citation, paper_id) in ScholarSpider.page2_links:
                        if citation == "":
                            continue
                        citation_bib_link = Bibtex(citation)  # Create object that uses Selenium
                        c_list = citation_bib_link.get_all_bibtex_links()
                        bib_link_total.append(c_list)

                        for url in c_list:
                            ScholarSpider.citation_dict[url] = paper_id
                            # Could paper id be a list -> abbiamo verificato che anche se bibtex uguale per id
                            # gli url sono diversi

                    for lin in bib_link_total:
                        for url in lin:
                            yield scrapy.Request(url, callback=self.parse3,
                                                 meta={'id': ScholarSpider.citation_dict.get(url)})
                        ScholarSpider.i = ScholarSpider.i + 1
                else:
                    for (citation, paper_id) in ScholarSpider.page2_links:
                        if citation == "":
                            continue
                        yield scrapy.Request(citation, callback=self.parse4,
                                             meta={'id': paper_id})

            try:
                paper_journal = paper.css("div.gs_gray::text").extract()[1]
            except IndexError:
                paper_journal = "-"
            paper_year = paper.css("span.gsc_a_h.gsc_a_hc.gs_ibl::text").get()
            paper_ncit = paper.css("a.gsc_a_ac.gs_ibl::text").extract()
            if not paper_ncit:
                paper_ncit = [0]
            ref = paper.css("td.gsc_a_c a.gsc_a_ac.gs_ibl::attr(href)").get()
            ScholarSpider.page2_links.append((str(ref), p_ID))

            # ScholarSpider.hash_list.append(p_ID)

            item = PublicationItem()
            item['Title'] = paper_title
            item["p_ID"] = p_ID
            item['Authors'] = paper_authors
            item['Journal'] = paper_journal
            item['Year'] = paper_year
            item['N_Citations'] = paper_ncit[0]
            item["a_ID"] = ScholarSpider.a_id
            yield item

        ScholarSpider.start += ScholarSpider.page_size
        next_page = ScholarSpider.start_urls[0] + "&cstart={}&pagesize={}".format(ScholarSpider.start,
                                                                                  ScholarSpider.page_size)
        yield scrapy.Request(next_page, callback=self.parse1)

    def parse3(self, response):
        item = BibTeXItem()
        item["p_ID"] = response.meta.get('id')
        item["Type"] = response.text
        yield item

    def parse4(self, response):
        for paper in response.css('div.gs_ri'):
            item = CitationItem()
            item["p_ID"] = response.meta.get('id')
            item["Title"] = paper.css('h3.gs_rt a::text').extract_first()
            item["c_ID"] = hash(paper.css('h3.gs_rt a::text').extract_first())
            try:
                item["Author"] = paper.css('div.gs_a a::text').extract()
            except:
                item["Author"] = ""
            item["Paper"] = paper.css('div.gs_a::text').extract()
            yield item

            next_page = response.css('a.gs_nma::attr(href)').extract()[1]
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse4)
