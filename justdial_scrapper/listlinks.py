import datetime

import pandas as pd
from selenium.webdriver.common.keys import Keys
import numpy as np
from selenium import webdriver
import selenium.webdriver.support.ui as ui

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json, time

categories = [
    (50, 'Grocery-Stores/nct-10237947', 'Gurugram'),
    (50, 'Grocery-Stores/nct-10237947', 'Noida'),
    (50, 'Grocery-Stores/nct-10237947', 'Faridabad'),

    (50, 'Chemists/nct-10096237', 'Delhi'),
    (50, 'Chemists/nct-10096237', 'Gurugram'),
    (50, 'Chemists/nct-10096237', 'Noida'),
    (50, 'Chemists/nct-10096237', 'Faridabad'),

    (50, 'Car-Tyre-Dealers/nct-10078913', 'Delhi'),
    (50, 'Car-Tyre-Dealers/nct-10078913', 'Gurugram'),
    (50, 'Car-Tyre-Dealers/nct-10078913', 'Noida'),
    (50, 'Car-Tyre-Dealers/nct-10078913', 'Faridabad'),

    (50, 'Two-Wheeler-Tyre-Dealers/nct-10967092', 'Delhi'),
    (50, 'Two-Wheeler-Tyre-Dealers/nct-10967092', 'Gurugram'),
    (50, 'Two-Wheeler-Tyre-Dealers/nct-10967092', 'Noida'),
    (50, 'Two-Wheeler-Tyre-Dealers/nct-10967092', 'Faridabad'),

    (50, 'Motorcycle-Accessory-Dealers/nct-10329700', 'Delhi'),
    (50, 'Motorcycle-Accessory-Dealers/nct-10329700', 'Gurugram'),
    (50, 'Motorcycle-Accessory-Dealers/nct-10329700', 'Noida'),
    (50, 'Motorcycle-Accessory-Dealers/nct-10329700', 'Faridabad'),
]

browser = webdriver.Chrome("/Users/abhishek/chromedriver")
initial_url = 'https://www.justdial.com/%s/%s/page-%s'

for pages, category, city in categories:
    data = []
    for i in range(pages):
        url = initial_url % (city, category, i + 1)
        print(url)
        browser.get(url)

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            print(browser.current_url != url, browser.current_url, url)
            if browser.current_url != url:
                browser.get(url)
                continue
            else:
                break

        lists = browser.find_element_by_xpath('//*[@id="tab-5"]/ul').find_elements_by_tag_name('li')

        for l in lists:
            try:
                # ui.WebDriverWait(browser, 150).until(
                #     lambda browser: browser.find_element_by_xpath('//*[@id="newphoto0"]/span'))
                data.append({'category': category, 'link': l.get_attribute('data-href')})
            except Exception as e:
                print(2, e)
                try:
                    browser.execute_script("closePopUp('best_deal_div');")
                    browser.execute_script("$('#best_deal_div').remove();")
                    browser.execute_script("$('$('body > div.b-modal.__b-popup1__').remove();")
                except:
                    pass
    with open('/Users/abhishek/Desktop/justdial_links/%s.json' % (category+city).replace('/', ''), 'w') as outfile:
        json.dump(data, outfile)