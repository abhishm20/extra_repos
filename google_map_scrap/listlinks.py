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
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

categories = [
    "https://www.google.co.in/maps/search/pet+care/"
]

browser = webdriver.Chrome("/Users/abhishek/chromedriver")
initial_url = 'https://www.justdial.com/%s/%s/page-%s'

overlay_xpath = '//*[@id="pane"]/div/div[1]/div/div/div[4]/div[4]'

next_button_xpath = '//*[@id="n7lv7yjyC35__section-pagination-button-next"]'


def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


for url in categories:
    browser.get(url)

    wait = WebDriverWait(browser, 50)
    men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, next_button_xpath)))

    listing = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]')

    name_list = []
    for div in listing.find_elements_by_css_selector('div'):
        if div.get_attribute('role') == 'listitem':
            name_list.append(div.find_element_by_css_selector('h3').text)

    for name in name_list:
        wait = WebDriverWait(browser, 10)
        men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, next_button_xpath)))

        listing = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]')
        for div in listing.find_elements_by_css_selector('div'):
            if div.get_attribute('role') == 'listitem' and div.find_element_by_css_selector('h3').text == name:
                name_list.append(div.find_element_by_css_selector('h3').text)
                print(div.find_element_by_css_selector('h3').text)
                div.click()
                wait = WebDriverWait(browser, 50)
                wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pane > div > div.widget-pane-content.scrollable-y > div > div')))
                row_container = browser.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div')
                rows = row_container.find_elements_by_tag_name('div')
                print(len(rows))
                for d in rows:
                    if d.get_attribute('data-section-id') == 'pn0':
                        print(d.text)
                        break
                browser.find_element_by_css_selector('#pane  button.section-back-to-list-button').click()
                break
    # with open('/Users/abhishek/Desktop/justdial_links/%s.json' % (category+city).replace('/', ''), 'w') as outfile:
    #     json.dump(data, outfile)