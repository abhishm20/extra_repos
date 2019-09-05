import datetime
import json
import re
import os
import pandas as pd
from selenium.webdriver.common.keys import Keys
import numpy as np
from selenium import webdriver
import selenium.webdriver.support.ui as ui

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome("/Users/abhishek/chromedriver")

data = []
columns = ["Shop Name", "Number", "Address", "Tags", "URL", "Rating", "Rates", "Image Links"]

directory = '/Users/abhishek/Desktop/justdial_links/'
files = os.listdir(directory)

for file in files:
    writer = pd.ExcelWriter(
        '/Users/abhishek/Desktop/justdial_links/%s.xlsx' % file,
        engine='openpyxl')
    f = open(os.path.join(directory, file))
    links = json.load(f)
    links = [a for a in links if a]
    for index, l in enumerate(links):
        print index, l['link']
        if not l['link']:
            continue

        browser.get(l['link'])
        image_links = []
        name = ""
        rating = ""
        rates = ""
        address = ""
        tags = ""

        try:
            try:
                browser.execute_script("removedn('showmore')")
            except:
                pass
            try:
                name = browser.find_element_by_xpath(
                    '//*[@id="setbackfix"]/div[1]/div/div[1]/div[2]/div/div/h1/span/span').text
            except:
                pass
            try:
                rating = browser.find_element_by_xpath(
                    '//*[@id="setbackfix"]/div[1]/div/div[1]/div[2]/div/div/div/span/span[1]/span[1]/span').text
            except:
                pass

            try:
                rates = browser.find_element_by_xpath(
                    '//*[@id="setbackfix"]/div[1]/div/div[1]/div[2]/div/div/div/span/span[2]/span[1]').text
            except:
                pass

            try:
                address = browser.find_element_by_xpath('//*[@id="fulladdress"]/span').text
            except:
                pass


            try:
                tags_span = browser.find_element_by_xpath('//*[@id="comp-contact"]/li[2]/span[3]')
                tags = ", ".join([a.text for a in tags_span.find_elements_by_tag_name('a')])
            except:
                pass

            try:
                images = browser.find_element_by_xpath('//*[@id="gal_img"]/ul').find_elements_by_tag_name("li")
                for index, image in enumerate(images):
                    try:
                        image.click()
                    except:
                        pass
                    for img in browser.find_element_by_xpath('//*[@id="ImageHost"]').find_elements_by_tag_name("a"):
                        image = img.find_element_by_tag_name("img")
                        image_links.append(image.get_attribute("src").split('?')[0])
            except:
                pass

            browser.get(l['link'].replace('://www.', '://t.'))
            number = browser.find_element_by_css_selector('#shell span.dpvstph > span').text
            number = re.sub("[+,(,),-]", '', number)
            print([name, number, address, tags, l['link'], rating, rates, ", ".join(image_links)])
            data.append([name, number, address, tags, l['link'], rating, rates, ", ".join(image_links)])
        except Exception as e:
            print 2, e
            try:
                browser.execute_script("closePopUp('best_deal_div');")
                browser.execute_script("$('#best_deal_div').remove();")
                browser.execute_script("$('$('body > div.b-modal.__b-popup1__').remove();")
            except:
                pass

    df = pd.DataFrame(np.array(data), columns=columns)
    df.to_excel(writer, "Listing")
    writer.save()
    print "Done"
