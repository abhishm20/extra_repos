# -*- coding: utf-8 -*-
import requests, json
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import pandas as pd
import re
from datetime import datetime
import requests


browser = webdriver.Chrome("/Users/abhishek/chromedriver")

delay = 30


def only_number(value):
    regex = re.compile('[^0-9]')
    return regex.sub('', value)


def only_char(value):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', value)


def only_decimal(value):
    regex = re.compile('[^0-9.]')
    return regex.sub('', value)


dir = '/Users/abhishek/Desktop/olx/sbi/links'

base_dir = '/Users/abhishek/Desktop/olx/sbi/images/'

filepath = '/Users/abhishek/Desktop/olx/sbi/links/Noida.json'
file_data = open(filepath, 'r+')
data_list = json.loads(file_data.read())
for s,a in enumerate(data_list[1:100]):
    print s, len(data_list)
    row = {}
    data = json.loads(json.loads(a['d'])[0])[0]

    url = 'https://www.sbirealty.in/property/%s/property-for-sale/%s/%s' % (data['CityName'].lower(), data['ProjectName'].lower().replace(" ", "-", 100), data['ProjectID'].lower())
    print url
    browser.get(url)

    try:
        browser.execute_script("window.scrollTo(0, 10000000)")
    except:
        pass

    delay = 25  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sync1 > div.owl-wrapper-outer > div > div:nth-child(1) > div > img')))
    except TimeoutException:
        print "Main is taking too long"
        continue

    project_root_folder = os.path.join(base_dir, '%s_%s_%s' % (data['ProjectName'], data['CityName'], ''))
    if not os.path.exists(project_root_folder):
        os.mkdir(project_root_folder)

    if not os.path.exists(os.path.join(project_root_folder, 'project')):
        os.mkdir(os.path.join(project_root_folder, 'project'))
    if not os.path.exists(os.path.join(project_root_folder, 'project', 'project_image')):
        os.mkdir(os.path.join(project_root_folder, 'project', 'project_image'))
    if not os.path.exists(os.path.join(project_root_folder, 'unit')):
        os.mkdir(os.path.join(project_root_folder, 'unit'))

    delay = 15  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#fplan > div > div.tab-content')))
    except TimeoutException:
        continue

    # Top images
    top_images = []
    try:
        images = browser.find_element_by_css_selector(
            '#sync1 > div.owl-wrapper-outer > div').find_elements_by_css_selector('div.owl-item')
    except Exception as e:
        print e
        images = []

    count = 0
    for i in images:
        image = i.find_element_by_tag_name('img').get_attribute('src')
        if 'elevation' in image.lower():
            print 1, image
            if not os.path.exists(os.path.join(project_root_folder, 'project', "Main_1.jpg")):
                r = requests.get(image)
                with open(os.path.join(project_root_folder, 'project', "Main_1.jpg"), 'wb') as f:
                    f.write(r.content)
        else:
            count += 1
            print 2, image
            if not os.path.exists(os.path.join(project_root_folder, 'project', 'project_image', str(count)+".jpg")):
                r = requests.get(image)
                with open(os.path.join(project_root_folder, 'project', 'project_image', str(count)+".jpg"), 'wb') as f:
                    f.write(r.content)

    # try:
    #     units = browser.find_element_by_css_selector('#fplan > div > ul').find_elements_by_tag_name('li')
    # except Exception as e:
    #     print e
    #     units = []
    # units = [a.text for a in units]
    # print units
    try:
        floor_div = browser.find_element_by_css_selector('#fplan > div > div.tab-content')
    except:
        continue

    for a in floor_div.find_elements_by_css_selector('div.tab-pane > div'):
        id = only_number(a.get_attribute('id'))
        name = str(id) + "BHK_1"
        if not os.path.exists(os.path.join(project_root_folder, 'unit', name)):
            os.mkdir(os.path.join(project_root_folder, 'unit', name))
        if not os.path.exists(os.path.join(project_root_folder, 'unit', name, 'floor_plan')):
            os.mkdir(os.path.join(project_root_folder, 'unit', name, 'floor_plan'))

        try:
            images = a.find_elements_by_tag_name('a')
        except:
            images = []
        for index, img in enumerate(images):
            print 3, img.get_attribute('href')
            if not os.path.exists(os.path.join(project_root_folder, 'unit', name, 'floor_plan', str(index + 1) + ".jpg")):
                r = requests.get(img.get_attribute('href'))
                with open(os.path.join(project_root_folder, 'unit', name, 'floor_plan', str(index + 1) + ".jpg"), 'wb') as f:
                    f.write(r.content)
