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

browser.get("https://en.wikipedia.org/wiki/List_of_Indian_dishes")
# print browser.execute_script("return jQuery.active == 0")
time.sleep(1)

# elem = browser.find_element_by_tag_name("mw-category-group")


typeName = browser.find_elements_by_tag_name('tr')
# todate = datetime.datetime.now().strftime("%Y-%m-%d")
# data = []
# columns = ["Title", "Site Name", "Item Name", "Rate", "Unit"]

for i in range(len(typeName)):
    print typeName[i].text
#
# writer = pd.ExcelWriter('/Users/abhishek/Desktop/B2C-Rates/Nature\'s Basket - '+datetime.datetime.now().strftime("%Y-%m-%d - %f")+'.xlsx')
# data = np.array(data)
# df = pd.DataFrame(data, columns=columns)
# df.to_excel(writer, todate)
# writer.save()
print "Done"
