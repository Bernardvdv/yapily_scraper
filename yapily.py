import csv
import time
import constants

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_values():
    details = {}
    for i in range(208):
        try:
            for x in range(10):
                time.sleep(1)
                input_number = driver.find_element(By.NAME, 'pageNumber')
                input_number.clear()
                input_number.send_keys(str(i))
                time.sleep(1)
                # Change page limit to 100
                # select = Select(driver.find_element(By.ID, "limit-dropdown"))
                # select.select_by_visible_text('100 items')

                # Scroll to the top
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
                table = driver.find_element(By.XPATH, "//table[@data-test-id='table-insitutions']")
                rows = table.find_elements(By.XPATH, ".//tr")
                time.sleep(1)
                rows[x].click()
                time.sleep(1)
                html = driver.page_source
                soup2 = BeautifulSoup(html, features="lxml")

                try:
                    bank_name = soup2.find("div", {"class": "detail-content-name"}).text.strip()
                    # bank_name = name
                except:
                    bank_name = "Not Found"
                    pass

                try:
                    bank_full_name = soup2.find("div", {"id": "fullName"})
                    bank_full_name = bank_full_name.find("div", {"class": "detail-content-name"}).text.strip()
                except:
                    bank_full_name = "Not Found"
                    pass

                try:
                    bank_id = soup2.find("div", {"id": "id"})
                    bank_id = bank_id.find("div", {"class": "d-inline"}).text.strip()
                except:
                    bank_id = "Not Found"
                    pass

                try:
                    bank_bic = soup2.find("div", {"id": "bic"})
                    bank_bic = bank_bic.find("div", {"class": "d-inline"}).text.strip()
                except:
                    bank_bic = "Not Found"
                    pass

                try:
                    env = soup2.find("div", {"id": "environmentType"})
                    env = env.find("div", {"class": "d-inline"}).text.strip()
                except:
                    env = "Not Found"
                    pass

                try:
                    bu_type = soup2.find("div", {"id": "businessTypesList"})
                    bu_type = bu_type.find_all('li')
                    bu_type = [x.text for x in bu_type]
                except:
                    bu_type = "Not Found"
                    pass

                try:
                    pis = soup2.find("div", {"id": "pisFeaturesList"})
                    pis = pis.find_all('li')
                    pis = [x.text.strip() for x in pis]
                except:
                    pis = "Not Found"
                    pass

                try:
                    ais = soup2.find("div", {"id": "aisFeaturesList"})
                    ais = ais.find_all('li')
                    ais = [x.text.strip() for x in ais]
                except:
                    ais = "Not Found"
                    pass

                try:
                    countries = soup2.find("div", {"id": "countriesList"})
                    countries = countries.find_all('li')
                    countries = [x.text.strip() for x in countries]
                except:
                    countries = "Not Found"
                    pass

                details[bank_name] = {}
                details[bank_name]['Full_name'] = bank_full_name
                details[bank_name]['ID'] = bank_id
                details[bank_name]['BIC'] = bank_bic
                details[bank_name]['Environment'] = env
                details[bank_name]['Business_Type'] = bu_type
                details[bank_name]['PIS'] = pis
                details[bank_name]['AIS'] = ais
                details[bank_name]['Countries'] = countries
                driver.back()
        except:
            pass

    return details


driver = webdriver.Chrome(executable_path='/Users/bernard/private_projects/yapily_scraper/chromedriver')
driver.get("https://accounts.yapily.com/login")

username = driver.find_element("name", "email")
password = driver.find_element("name", "password")
username.send_keys(constants.USER)
password.send_keys(constants.PASSWORD)
driver.find_element(By.CLASS_NAME, "button-text").click()

time.sleep(1)
driver.get("https://console.yapily.com/institutions")
time.sleep(1)

values1 = get_values()

with open('output.csv', 'w') as output:
    writer = csv.writer(output)
    writer.writerow([
        'Bank',
        'Full Name',
        'ID',
        'BIC',
        'Environment',
        'Business_Type',
        'PIS',
        'AIS',
        'Countries',
    ])

    for value, keys in values1.items():
        writer.writerow([
            value,
            keys['Full_name'],
            keys['ID'],
            keys['BIC'],
            keys['Environment'],
            keys['Business_Type'],
            keys['PIS'],
            keys['AIS'],
            keys['Countries']
        ])
