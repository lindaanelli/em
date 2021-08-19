from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class Bibtex:

    def __init__(self, citation):

        self.citation = citation

    def get_all_bibtex_links(self):
        try:

            webdriver.Chrome()
            driver = webdriver.Chrome()

            # options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            link_to_click = []
            # text_list = []
            # temp = []
            start = 0
            i = 0

            while True:

                url = self.citation + "&start={}".format(start)
                driver.get(url)

                WebDriverWait(driver, 50)

                control = driver.find_element(By.ID, "gs_res_ccl_mid").text
                control = str(control)
                if not control:
                    break

                for x in driver.find_elements_by_css_selector("a.gs_or_cit.gs_nph"):
                    WebDriverWait(driver, 10)
                    x.click()

                    WebDriverWait(driver, 20).until(ec.visibility_of_all_elements_located((By.ID, "gs_citt")))

                    # for element in search:
                    #   title = element.find_elements_by_css_selector('div.gs_citr')
                    #    types = element.find_elements_by_css_selector("th.gs_cith")

                    #    for t in title:
                    #       t2 = t.text
                    #        temp.append([str(t2)])

                    #   for typ in types:
                    #        typ2 = typ.text
                    #        temp.append([str(typ2)])
                    #    text_list.append(temp.copy())
                    #    temp.clear()

                    bibtex = driver.find_elements_by_css_selector("a.gs_citi")
                    link_to_click.append(bibtex[0].get_attribute("href"))
                    driver.implicitly_wait(10)
                    close = driver.find_element_by_css_selector("span.gs_ico")
                    driver.implicitly_wait(10)
                    ActionChains(driver).move_to_element(close).click(close).perform()

                start = start + 10
                i = 1 + i

            driver.stop_client()
            driver.close()
            driver.quit()
            print(link_to_click)
            return link_to_click
        except NoSuchElementException:
            print("ERROR DURING SCRAPING WITH SELENIUM. PLEASE CHANGE IP ADDRESS")
            return NoSuchElementException
