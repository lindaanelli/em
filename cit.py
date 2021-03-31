from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


text_list = []
temp = []

# options = webdriver.Chrome()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get("https://scholar.google.com/scholar?oi=bibs&hl=en&cites=10972803237645083033")

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

    close = driver.find_element_by_css_selector("span.gs_ico")
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(close).click(close).perform()


driver.quit()
print(text_list)


# TODO: go to page 2
# TODO: BibTeX
# TODO: save list as json