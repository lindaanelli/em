from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException




text_list = []
temp = []
bib = []
title = []
i = 0

webdriver.Chrome()
driver = webdriver.Chrome()

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

driver.get("https://scholar.google.com/scholar?oi=bibs&hl=en&cites=10972803237645083033")

for x in driver.find_elements_by_css_selector("a.gs_or_cit.gs_nph"):
    WebDriverWait(driver, 10)
    title.append(x)
try:
    while True:
        try:
            title[i].click()
        except StaleElementReferenceException:
            driver.refresh()
            for x in driver.find_elements_by_css_selector("a.gs_or_cit.gs_nph"):
                WebDriverWait(driver, 10)
                title.append(x)
                title[i].click()
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
        bibtex[0].click()
        content = driver.find_element_by_css_selector("body")
        content = content.text
        print(content)
        bib.append([content])
        driver.back()

        driver.implicitly_wait(10)
        close = driver.find_element_by_css_selector("span.gs_ico")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(close).click(close).perform()
        i = i + 1
except IndexError:
    pass


driver.quit()
print(text_list)

