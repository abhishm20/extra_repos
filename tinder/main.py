import random

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# no need to login everytime you login
CHROME_PROFILE_PATH = '/Users/abhishek/projects/ext/tinder/profile'
CHROME_DRIVER_PATH = '/Users/abhishek/chromedriver'

driver_options = webdriver.ChromeOptions()
driver_options.add_argument("user-data-dir={0}".format(CHROME_PROFILE_PATH))

# setting up Chrome with selenium
browser = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=driver_options)

url = 'https://tinder.com/'

like_btn = '//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[4]'

browser.get(url)

index = 1
while True:
    try:
        btn = browser.find_element_by_xpath(like_btn)
        browser.find_element_by_css_selector('body').send_keys(Keys.RIGHT)
        print 'liking ... ' + str(index)
        index += 1
        time.sleep(random.uniform(1, 3.7))
    except NoSuchElementException as e:
        time.sleep(5)
