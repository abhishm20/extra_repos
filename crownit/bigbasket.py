import requests
import sys
import numpy as np
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import json
from pprint import pprint

with open('cat_big.json') as data_file:
    data = json.load(data_file)

pprint(data)


exit(0)
browser = webdriver.Chrome("/Users/abhishek/chromedriver")

browser.get("http://www.bigbasket.com/cl/fruits-vegetables")
time.sleep(1)

# Skip
browser.find_element_by_name("cityquery").send_keys("Delhi-Noida")
time.sleep(1)
skipBtn = browser.find_element_by_name("skipandexplore").click()
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 100
wait = WebDriverWait(browser, 30)

while no_of_pagedowns:
    page_title = browser.find_elements_by_class_name('uiv2-page-title')
    if page_title[len(page_title) - 1].text == 'Page 13':
        break
    print 100 - no_of_pagedowns
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(.5)
    if browser.find_element_by_id("next-product-page") and browser.find_element_by_id("next-product-page").is_displayed():
        browser.find_element_by_id("next-product-page").click()
    time.sleep(.5)
    no_of_pagedowns -= 1


blocks = browser.find_elements_by_css_selector(".uiv2-shopping-lis-sku-cards")


todate = datetime.datetime.now().strftime("%Y-%m-%d")
data = []
columns = ["Date", "Site Name", "Item Name", "Rate"]


for a in blocks:
    d = a.text.split('\n')
    if(d[1] == "FRESHO"):
        a = [todate, "Bigbasket", d[2], d[3]]
        data.append(a)
    elif(d[2] == "FRESHO"):
        a = [todate, "Bigbasket", d[3], d[4]]
        data.append(a)

writer = pd.ExcelWriter('/Users/abhishek/Desktop/B2C-Rates/Bigbasket - '+datetime.datetime.now().strftime("%Y-%m-%d - %f")+'.xlsx')
data = np.array(data)
df = pd.DataFrame(data, columns=columns)
df.to_excel(writer, todate)
writer.save()
print "Done"
