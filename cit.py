from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


link_to_click = []
text_list = []
temp = []
bib = []
final_bib = []
start = 0
i = 0


webdriver.Chrome()
driver = webdriver.Chrome()

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

while True:

    url = "https://scholar.google.it/scholar?oi=bibs&hl=it&cites=9931762518269776070&start={}".format(start)
    driver.get(url)

    control = driver.find_element(By.ID, "gs_res_ccl_mid").text
    control = str(control)
    if not control:
        break

    for x in driver.find_elements_by_css_selector("a.gs_or_cit.gs_nph"):
        WebDriverWait(driver, 10)
        x.click()

        search = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.ID, "gs_citt")))

        for element in search:
            title = element.find_elements_by_css_selector('div.gs_citr')
            types = element.find_elements_by_css_selector("th.gs_cith")

            for t in title:
                t2 = t.text
                temp.append([str(t2)])

            for typ in types:
                typ2 = typ.text
                temp.append([str(typ2)])
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

for pub in bib:
    for element in pub:
        stripped_line = element.replace('\n', '')
        final_bib.append([stripped_line])


driver.quit()
print(text_list)
print(final_bib)


# TODO: go to page 2
# TODO: save list as json
