import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json


browser = webdriver.Chrome("/Users/abhishek/chromedriver")


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


url = 'https://www.magicbricks.com/Real-estate-projects-search/ALL-RESIDENTIAL'
browser.get(url)


delay = 30

while True:
    try:
        browser.execute_script("window.scrollTo(0, 10000000)")
    except:
        pass

    try:
        myElem = WebDriverWait(browser, delay).until(EC.invisibility_of_element_located((By.ID, 'moreResult-loader')))
    except TimeoutException:
        print "Loading took too much time!"

    rows = browser.find_elements_by_css_selector('.srpBlockListRow')
    if len(rows) >= 150:
        break

links = []

for a in browser.find_elements_by_css_selector('.srpBlockListRow'):
    links.append(a.find_element_by_css_selector('.proNameColm1 > a').get_attribute('href'))

with open('/Users/abhishek/Desktop/magicbricks.json', 'w') as f:
    json.dump(links, f)
