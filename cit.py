from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


link_to_click = []
text_list = []
temp = []
bib = []
start = 0
i = 0

webdriver.Chrome()
driver = webdriver.Chrome()

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

while i < 10:

    url = "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=10972803237645083033&start={}".format(start)
    driver.get(url)

    for x in driver.find_elements_by_css_selector("a.gs_or_cit.gs_nph"):
        WebDriverWait(driver, 10)
        x.click()

        search = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.ID, "gs_citt")))

        for element in search:
            title = element.find_elements_by_css_selector('div.gs_citr')

            for t in title:
                t2 = t.text
                temp.append(str(t2))
            text_list.append(temp.copy())
            temp.clear()

        bibtex = driver.find_elements_by_css_selector("a.gs_citi")
        link_to_click.append(bibtex[0].get_attribute("href"))
        driver.implicitly_wait(10)
        close = driver.find_element_by_css_selector("span.gs_ico")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(close).click(close).perform()

    start = start + 10
    i = 1 + i

for link in link_to_click:
    driver.get(link)
    content = driver.find_element_by_css_selector("body")
    content = content.text
    bib.append([content])


driver.quit()
print(bib)


# TODO: go to page 2
# TODO: BibTeX
# TODO: save list as json
