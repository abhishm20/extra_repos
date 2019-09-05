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

writer = pd.ExcelWriter(
            '/Users/abhishek/Desktop/Zomato-' + datetime.datetime.now().strftime("%Y-%m-%d - %f") + '.xlsx',
            engine='openpyxl')

india = 'https://www.zomato.com/india'
browser.get(india)
cities_ele = browser.find_elements_by_css_selector('section.mtop2 > :nth-child(2) > :nth-child(1) > *')

cities = []

for city in cities_ele:
    ele = city.find_element_by_tag_name('a')
    link = ele.get_attribute('href')
    city_name = ele.text
    cities.append({
        'link': link,
        'name': city_name
    })

count = 0

data = []
todate = datetime.datetime.now().strftime("%Y-%m-%d")
columns = ["Id", "Name", "Subzone", "Address", "Rating", "Vote", "Reviews", "Cousine", "Cost", "Timing", "Phone", "Site"]
ratingArray = []


for city in cities:
    url = city['link']+"/restaurants/"
    browser.get(url)
    pages = browser.find_element_by_css_selector('.pagination-number > :nth-child(1) > :nth-child(2)')
    page_nos = pages.text
    data = []
    for i in range(0, int(page_nos)):
        browser.get(url + '?page=' + str(i + 1))
        time.sleep(1)

        blocks = browser.find_elements_by_css_selector(".search-snippet-card")

        for a in blocks:
            count += 1
            try:
                id = a.find_element_by_css_selector("div.js-search-result-li").get_attribute('data-res_id')
            except:
                id = "id"
            try:
                name = a.find_element_by_css_selector("a.result-title.hover_feedback").text
            except:
                name = "name"
            try:
                subzone = a.find_element_by_css_selector("a.search_result_subzone").text
            except:
                subzone = "subzone"
            try:
                address = a.find_element_by_css_selector("div.search-result-address").text
            except:
                address = "address"
            try:
                cousine = a.find_element_by_css_selector("div.search-page-text > div").text.split('\n')[1]
            except:
                cousine = "cousine"
            try:
                cost = a.find_element_by_css_selector("div.res-cost").text.split("\n")[1]
            except:
                cost = "cost"
            try:
                timing = a.find_element_by_css_selector("div.res-timing").text.split("\n")[1]
            except:
                timing = "timing"
            try:
                phone = a.find_element_by_css_selector("a.res-snippet-ph-info").get_attribute('data-phone-no-str')
            except:
                phone = "phone"
            try:
                site = a.find_element_by_css_selector("a.result-title.hover_feedback").get_attribute('href')
            except:
                site = "site"
            try:
                ratingArray = a.find_element_by_css_selector("div.floating.search_result_rating").text.split('\n')
                rating = ratingArray[0]
                vote = ratingArray[1]
                reviews = ratingArray[2]
            except:
                rating = "rating"
                vote = "vote"
                reviews = "reviews"

            row = [id, name, subzone, address, rating, vote, reviews, cousine, cost, timing, phone, site]
            data.append(row)
            print count, name, subzone

    df = pd.DataFrame(np.array(data), columns=columns)
    df.to_excel(writer, city['name'])
    writer.save()
    print "Done"
