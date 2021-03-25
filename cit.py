from selenium import webdriver
import scrapy
from scrapy.http import Request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class CitationItem(scrapy.Field):
    Title = scrapy.Field()
    Format = scrapy.Field


class PButton(scrapy.Spider):
    name = "PButton"
    allowed_domains = ["google.com"]

    def start_requests(self):
        yield Request("https://scholar.google.com/scholar?oi=bibs&hl=en&cites=10972803237645083033",
                      callback=self.parse)

    def parse(self, response):

        driver = webdriver.Chrome()
        driver.get(response.url)
        for x in driver.find_elements_by_css_selector("a.gs_or_cit.gs_nph"):
            WebDriverWait(driver, 10)
            x.click()
            for name in response.css('div#gs_citt'):
                name_title = name.css("div.gs_citr::text").extract()
                name_format = name.css("th.gs_cith::text").extract()

                item = CitationItem()
                item["Title"] = name_title
                item["Format"] = name_format
                yield item
            close = driver.find_element_by_css_selector("span.gs_ico")
            driver.implicitly_wait(10)
            ActionChains(driver).move_to_element(close).click(close).perform()

        driver.quit()
