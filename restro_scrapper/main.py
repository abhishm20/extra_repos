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

browser = webdriver.Chrome("/Users/abhishek/chromedriver")

browser.get("http://www.hrani.net.in/hraniSearch/restsrch2.asp?Rest=&city=Noida&Cuisine=&paging=30")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

data = []
columns = ["Restaurant Name", "Email", "Other details", "Address", "Cuisine"]
links = []
for i in elem.find_elements_by_css_selector('td > font > a'):
    links.append(i.get_attribute('href'))


for l in links:
    browser.get(l)
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    name = elem.find_element_by_css_selector(':nth-child(3) > tbody > tr > td:nth-child(2)').text
    email = elem.find_element_by_css_selector(':nth-child(3) > tbody > tr:nth-child(7) > td > a').text
    details = elem.find_element_by_css_selector(':nth-child(3) > tbody > tr:nth-child(7) > td').text
    address = elem.find_element_by_css_selector(':nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(1)').text
    cuisine = elem.find_element_by_css_selector(':nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(2)').text
    data.append([name, email, details, address, cuisine])

todate = datetime.datetime.now().strftime("%Y-%m-%d")

writer = pd.ExcelWriter('/Users/abhishek/Desktop/restaurant-noida.xlsx')
data = np.array(data)
df = pd.DataFrame(data, columns=columns)
df.to_excel(writer, todate)
writer.save()
print "Done"
