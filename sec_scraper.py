import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# interpolate search URL
driver.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001166559&type=13f')
# find the first 13f docs button
ele = driver.find_element_by_xpath("//a[@id='documentsbutton']")
# click it
ele.click()

try:
    ele_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "table.xml"))
    )
finally:
    ele_link.click()


print(ele_link)

# request = requests.get(ele_link)
# print(request.text)

# def cik_search(cik):
#     request = requests.get(
#         f'https://www.sec.gov/cgi-bin/browse-edgar?CIK={cik}$type=13f')
#     return request.text


# print(cik_search('VOYA'))
