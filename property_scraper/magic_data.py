import re

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome("/Users/abhishek/chromedriver")
import json

path = '/Users/abhishek/Desktop/magicbricks.json'
links = json.loads(open(path).read())

data_list = []
for x,link in enumerate(links):
    print x
    browser.get(link)

    try:
        browser.execute_script("window.scrollTo(0, 10000000)")
    except:
        pass

    # try:
    #     browser.execute_script('xid99.loadMap();')
    # except:
    #     pass
    #
    delay = 5  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.xidPrmAmnInner')))
    except TimeoutException:
        print "Loading took too much time!"

    data = dict()

    try:
        data['Project_Name'] = browser.find_element_by_xpath("/html/body/div[13]/div[2]/div/div/div[1]/div[2]/div/h1").text
    except:
        try:
            data['Project_Name'] = browser.find_element_by_xpath(
                '/html/body/div[13]/div[1]/div/div/div/div[1]/div[2]/div/h1').text
        except:
            continue

    data['Operation_Type'] = 'Project Add'

    try:
        city = browser.find_element_by_xpath("/html/body/div[13]/div[2]/div/div/div[1]/div[2]/div/span").text.split(',')
        data['City'] = city[len(city) - 1]
    except:
        data['City'] = ''

    # Photos
    try:
        code = browser.find_element_by_xpath('//*[@id="detailFrontPhotoWidget"]/div[2]/span').get_attribute('onclick')
        browser.execute_script(code)
    except:
        pass

    delay = 30  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.xidPrmAmnInner')))
    except TimeoutException:
        print "Loading took too much time!"

    try:
        images = []
        for i in browser.find_element_by_css_selector('#propertyImageSliderThumb > ul').find_elements_by_tag_name('li'):
            try:
                images.append(i.find_element_by_tag_name('img').get_attribute('src'))
            except Exception as e:
                pass
        data['Image_Folder'] = ', '.join(images)
    except:
        data['Image_Folder'] = ''

    try:
        browser.execute_script('closePhotoMap();')
    except:
        pass

    data['Number_Of_Units'] = ''
    data['Total_Number_Of_Blocks'] = ''
    try:
        unit_towers = browser.find_element_by_xpath(
            '//*[@id="overNav"]/div[1]/div[1]/div[1]/div[1]/table/tbody/tr/td[2]/div').text.split('\n')
        for a in unit_towers:
            if 'unit' in a.lower():
                data['Number_Of_Units'] = a
            if 'tower' in a.lower():
                data['Total_Number_Of_Blocks'] = a
    except:
        pass

    try:
        data['Specifications'] = browser.find_element_by_xpath('//*[@id="detNav"]/div[6]/div[1]/div/div').text
    except:
        data['Specifications'] = ''

    # bank_approvals = []
    # bank_approvals_ele = browser.find_elements_by_css_selector('.bankBodr')
    # for bank_approval in bank_approvals_ele:
    #     bank_approvals.append(bank_approval.find_element_by_tag_name('img').get_attribute('title'))
    # data['Loan_Approvals'] = ','.join(bank_approvals)

    try:
        data['Amenities'] = browser.find_element_by_xpath(
            '//*[@id="normalAminities"]').text
    except:
        data['Amenities'] = ''

    try:
        address = browser.find_element_by_xpath("/html/body/div[13]/div[2]/div/div/div[1]/div[2]/div/span").text.split(
            ',')
        data['Address'] = ",".join(city[1:])
    except:
        data['Address'] = ""

    try:
        for a in browser.find_element_by_xpath('//*[@id="detNav"]/div[1]/div/div[1]').find_elements_by_tag_name('meta'):
            if a.get_attribute('itemprop') == 'longitude':
                data['Lon'] = a.get_attribute('content')
            if a.get_attribute('itemprop') == 'latitude':
                data['Lat'] = a.get_attribute('content')
    except:
        data['Lat'] = ''
        data['Lon'] = ''

    try:
        data['Construction_Status'] = browser.find_element_by_css_selector(
            '#overNav > div.newChildWidth > div:nth-child(1) > div > div.newPiceBlockSec.sec4 > div.secValueUp').text
    except:
        data['Construction_Status'] = ''

    try:
        data['Highlights'] = browser.find_element_by_xpath('//*[@id="detNav"]/div[1]/div/div[2]/div/div[1]/div/ul').text
    except:
        data['Highlights'] = ''

    try:
        price_range = browser.find_element_by_css_selector('body > div.projectDetWrap.openInPop > div.middleData.bannerBlockUp > div > div > div.projectPriceCont > div.projectPrice').text.split('to')
        data['Prices_Min'] = price_range[0]
        data['Prices_Max'] = price_range[1]
    except:
        pass

    try:
        data['Builder'] = browser.find_element_by_xpath('//*[@id="aboutNav"]/div[1]/div[1]/a').text
    except:
        data['Builder'] = ''

    units = []
    try:
        units = browser.find_element_by_xpath('//*[@id="unitSlider"]').find_elements_by_tag_name('li')
    except:
        pass
    for unit in units:
        sub_data = {}
        try:
            sub_data['Unit_Name'] = unit.find_element_by_css_selector('div.propDtls > div.bed').text
        except Exception as e:
            pass
        try:
            sub_data['Unit_Carpet_Area'] = unit.find_element_by_css_selector('div.propDtls > div.space').text
        except Exception as e:
            pass

        try:
            prop_type = browser.find_element_by_xpath('//*[@id="tabs-sale"]/ul/li[1]/div[1]/div[1]').text
            for a in ['Apartment', 'Villa', 'Row Houses', 'Builder Floor', 'Plot', 'Studio']:
                if re.search(a, prop_type, re.IGNORECASE):
                    sub_data['Unit_Property_Types'] = a
                    break
        except:
            sub_data['Unit_Property_Types'] = ''

        sub_data.update(data)
        sub_data['Operation_Type'] = 'Unit Add'
        data_list.append(sub_data)

    data_list.append(data)

df = pd.DataFrame(data_list)
df.to_csv('/Users/abhishek/Desktop/magicbricks_data.csv', encoding='utf-8')
