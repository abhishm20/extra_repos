# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, re, math
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome("/Users/abhishek/chromedriver")


def only_number(value):
    regex = re.compile('[^0-9]')
    return regex.sub('', value)


def only_char(value):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', value)


def only_decimal(value):
    regex = re.compile('[^0-9.]')
    return regex.sub('', value)

df = pd.read_csv('./proptiger.csv')

for i, row in df.iterrows():
    cityname = row['name'].lower()
    print cityname

    url = 'https://www.proptiger.com/%s/property-sale' % cityname
    browser.get(url)

    project_count = int(only_number(browser.find_element_by_css_selector('#serp-listing > div:nth-child(4) > div.js-listHeading > div > span').text))

    delay = 30

    links = []

    project_counter = 1
    page = 1
    while True:
        url = 'https://www.proptiger.com/%s/property-sale?page=%s' % (cityname,page)
        browser.get(url)

        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#serp-listing > div.projects-cont')))
        except TimeoutException:
            print "Loading took too much time!"

        try:
            rows = browser.find_element_by_css_selector('#serp-listing > div.projects-cont').find_elements_by_tag_name(
                'section')
        except:
            rows = []
        for row in rows:
            try:
                row = row.find_element_by_css_selector('.project-card-info-wrap')
                u = row.get_attribute('data-url')
                links.append(u)
                project_counter += 1
            except Exception as e:
                pass

        page += 1
        if project_counter >= project_count:
            break


    with open('/Users/abhishek/Desktop/olx/proptiger/links/%s.json' % cityname, 'w') as f:
        json.dump(links, f)
