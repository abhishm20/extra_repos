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

browser.get("https://www.zopnow.com/vegetables-c.php")
time.sleep(1)

# Skip
browser.find_element_by_class_name("js-showpincode").click()
time.sleep(1)
browser.find_element_by_id("pincodeInput").send_keys("110033")
time.sleep(1)
browser.find_element_by_id("pincodeButton").click()
time.sleep(1)

elem = browser.find_element_by_css_selector(".selected3")

item_len = int(elem.text.split("\n")[0])

no_of_pagedowns = 20

while no_of_pagedowns:
    print item_len - no_of_pagedowns
    browser.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    if(no_of_pagedowns >= item_len):
        break
    no_of_pagedowns += 20


blocks = browser.find_element_by_css_selector(".productListing > .jsProductContainer").find_elements_by_css_selector("div.itemDescription > h4")
print blocks[0].text
todate = datetime.datetime.now().strftime("%Y-%m-%d")
data = []
columns = ["Date", "Site Name", "Item Name", "Rate"]


for a in blocks:
    d = a.text.split('\n')
    if len(d) > 0:
        print a.text
        a = [todate, "Zopnow", d[1], d[0]]
        data.append(a)

writer = pd.ExcelWriter('/Users/abhishek/Desktop/B2C-Rates/Zopnow - '+datetime.datetime.now().strftime("%Y-%m-%d - %f")+'.xlsx')
data = np.array(data)
df = pd.DataFrame(data, columns=columns)
df.to_excel(writer, todate)
writer.save()
print "Done"
