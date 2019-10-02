import requests
import lxml
import time
import csv
import xmlschema
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# interpolate search URL
driver.get(
    'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001037766&type=13f')
# find the first 13f docs button and click it
ele = driver.find_element_by_xpath("//a[@id='documentsbutton']").click()

# wait for client html call to resolve to DOM
table_div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "tableFile")))


# use beautiful soup to find correct link
source_overview = driver.page_source
soup = BeautifulSoup(source_overview, "html.parser")

table = soup.find_all("table")[-1]
table_rows = table.find_all("tr")[1:]
documents = []

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    documents.append(row)

link = [document[2]
        for document in documents if
        document[3] == 'INFORMATION TABLE' and
        document[2][-3:] == 'xml']
if len(link) is not 1:
    print("This institution either leaves the reporting of their holdings to their subsidiaries, or they report in a manner that has not yet been codified")

xml_link = driver.find_element_by_link_text(link[0])
xml_link.click()
# print('before')
time.sleep(10)
# driver.implicitly_wait(20)
# print('after')
source_overview = driver.page_source


# print('source_overview', source_overview)
xml_soup = BeautifulSoup(source_overview, features='lxml')
body = xml_soup.find_all("body")
print(body)
# # request = requests.get(ele_link)
# print(request.text)

# def cik_search(cik):
#     request = requests.get(
#         f'https://www.sec.gov/cgi-bin/browse-edgar?CIK={cik}$type=13f')
#     return request.text


# print(cik_search('VOYA'))
