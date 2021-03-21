from selenium import webdriver
import scrapy
from scrapy.http import Request
from selenium.webdriver.support.ui import WebDriverWait


class PButton(scrapy.Spider):
    name = "PButton"
    allowed_domains = ["google.com"]

    def start_requests(self):
        yield Request("https://scholar.google.com/scholar?oi=bibs&hl=en&cites=10972803237645083033",
                                  callback=self.parse)

    def parse(self, response):
        driver = webdriver.Chrome()
        driver.get(response.url)
        sel = scrapy.Selector(text=driver.page_source)
        for x in driver.find_elements_by_css_selector("a.gs_or_cit.gs_nph"):
            x.click()
            WebDriverWait(driver, 10)

            links = sel.css("div.gs_md_bdy")
            for link in links:
                yield {
                    "Title": link.css("div.gs_citr::text").get()
                }

        driver.quit()
