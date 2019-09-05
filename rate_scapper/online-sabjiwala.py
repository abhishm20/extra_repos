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

browser.get("http://onlinesabjiwala.com/fruits-vegetables/vegetables.html?SID=5f33bdf4dd3a310611b6a77b522ef761&limit=all")
time.sleep(1)

# Skip

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 100
wait = WebDriverWait(browser, 30)

blocks = browser.find_elements_by_css_selector(".item-inner")


todate = datetime.datetime.now().strftime("%Y-%m-%d")
data = []
columns = ["Date", "Site Name", "Item Name", "Rate"]


for a in blocks:
    d = a.text.split('\n')
    # print a.text
    a = [todate, "Online Sabjiwala", d[1], d[2]]
    data.append(a)

writer = pd.ExcelWriter('/Users/abhishek/Desktop/B2C-Rates/Online Sabjiwala - '+datetime.datetime.now().strftime("%Y-%m-%d - %f")+'.xlsx')
data = np.array(data)
df = pd.DataFrame(data, columns=columns)
df.to_excel(writer, todate)
writer.save()
print "Done"
