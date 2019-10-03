import csv
import datetime
import lxml
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


def generate_tsv_from_13f(cik):

    today = datetime.datetime.now()
    modified_today = f'{today.year}_{today.month}_{today.day}'

    # instantiate selenium driver instance
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # interpolate search URL
    driver.get(
        f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=13f')

    try:
        ele = driver.find_element_by_xpath(
            "//a[@id='documentsbutton']").click()

    except NoSuchElementException as ex:
        print("That entity does not file a form 13F. They likely file a form N-Q, the code for which is in progress.")
        return

    # find the first 13f docs button and click it

    # wait for client html call to resolve to DOM
    table_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tableFile")))

    # use beautiful soup to find correct link
    source_overview = driver.page_source
    soup = BeautifulSoup(source_overview, "html.parser")

    # there are two tables on this page - we're looking for the second
    table = soup.find_all("table")[-1]

    # get all the rows in the table except for the headers
    table_rows = table.find_all("tr")[1:]

    documents = []

    # loop through the rows and generate an array from each cell,
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        # push it onto the empty array for later
        documents.append(row)

    # find the XML link using list comprehension
    link = [document[2]
            for document in documents if
            # assumption here that all 13fs will be labled as information table
            # in the ones I checked, this was true but... still an assumption
            document[3] == 'INFORMATION TABLE' and
            document[2][-3:] == 'xml']

    # handle the Black Rock edge case - they're an umbrella for a bunch
    # of other Black Rock mutual funds. Those funds report individually.
    if len(link) is not 1:
        # with open(f'{cik}.tsv', 'wt') as output:

        print('This institution either leaves the reporting of their holdings to their subsidiaries, or they report in a manner that has not yet been codified.')
        return

    # selenium to locate the link to the xml filing
    xml_link = driver.find_element_by_link_text(link[0])
    xml_link.click()

    # wait for client html request to resolve
    information_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "informationTable")))

    # generate HTML for beautiful soup to parse
    source_overview = driver.page_source

    # make the soup
    xml_soup = BeautifulSoup(source_overview, features='lxml')

    # parse the soup
    body = xml_soup.body
    table = body.div
    positions = table.find_all('infotable')

    output_array = []

    #  generate an object for each position and push it onto the empty array
    for position in positions:
        position_object = {}
        position_object['Name'] = position.nameofissuer.get_text()
        position_object['Share Class'] = position.titleofclass.get_text()
        position_object['Number of Shares'] = position.sshprnamt.get_text()
        output_array.append(position_object)

    # write the tsv
    with open(f'{cik}_{modified_today}.tsv', 'wt') as output:
        tsv_writer = csv.writer(output, delimiter='\t')
        tsv_writer.writerow(['Company', 'Share Class', 'Number of Shares'])
        for position in output_array:
            tsv_writer.writerow([
                position['Name'],
                position['Share Class'],
                position['Number of Shares']])

    print('TSV file written succesfully.')
    return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please pass one and only one CIK or ticker to the function")
    else:
        generate_tsv_from_13f(sys.argv[1])
