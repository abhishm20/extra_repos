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

browser.get("http://www.naturesbasket.co.in/Online-grocery-shopping/Fruits---Vegetables/5_0_0")
print browser.execute_script("return jQuery.active == 0")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 100
wait = WebDriverWait(browser, 30)

while no_of_pagedowns:
    print 100 - no_of_pagedowns
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(.5)
    wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))
    no_of_pagedowns -= 1

name_elems = browser.find_elements_by_class_name("search_Ptitle")
price_elems = browser.find_elements_by_class_name("search_PSellingP")
unit_elems = browser.find_elements_by_class_name("search_PSelectedSize")


todate = datetime.datetime.now().strftime("%Y-%m-%d")
data = []
columns = ["Date", "Site Name", "Item Name", "Rate", "Unit"]

for i in range(len(price_elems)):
    if(i < len(unit_elems)):
        unit = unit_elems[i].text
    else:
        unit = ""
    a = [todate, "Nature's Basket", name_elems[i].text, float(price_elems[i].text[1:]), unit]
    data.append(a)
    i += 1


writer = pd.ExcelWriter('/Users/abhishek/Desktop/B2C-Rates/Nature\'s Basket - '+datetime.datetime.now().strftime("%Y-%m-%d - %f")+'.xlsx')
data = np.array(data)
df = pd.DataFrame(data, columns=columns)
df.to_excel(writer, todate)
writer.save()
print "Done"
