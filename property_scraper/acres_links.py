# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from selenium import webdriver

browser = webdriver.Chrome("/Users/abhishek/chromedriver")


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


cities = ['ahmedabad',
'bangalore',
'bhubaneswar',
'chandigarh',
'chennai',
'coimbatore',
'jaipur',
'kolkata',
'mumbai',
'ncr',
'pune']

for name in cities:
    links = []
    url = 'https://www.99acres.com/new-projects-in-%s-ffid-page-1' % name
    browser.get(url)

    try:
        pages = browser.find_element_by_css_selector('.pgdiv').find_elements_by_tag_name('a')
        last_page = browser.find_element_by_css_selector('#results > div.pgdiv > a:nth-child(%s)' % str(len(pages) + 1))
        last_page_int = int(last_page.text)
    except:
        last_page_int = 0

    for i in range(last_page_int + 1):
        url = 'https://www.99acres.com/new-projects-in-%s-ffid-page-%s' % (name, str(i + 1))
        browser.get(url)

        print name,i
        try:
            ls = browser.find_elements_by_css_selector('.npsrp_card')
            for a in ls:
                links.append(a.find_element_by_css_selector('a.npt_titl_desc').get_attribute('href'))
        except:
            pass

    with open('/Users/abhishek/Desktop/olx/99acreslinks/%s-2.json' % name, 'w') as f:
        json.dump(links, f)
