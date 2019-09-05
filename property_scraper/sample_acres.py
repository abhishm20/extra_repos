import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import json, os


browser = webdriver.Chrome("/Users/abhishek/chromedriver")


def only_number(value):
    regex = re.compile('[^0-9]')
    return regex.sub('', value)


def only_char(value):
    regex = re.compile('[^a-zA-Z ]')
    return regex.sub('', value)


def only_decimal(value):
    if len(value.split('.')) > 2:
        value = ".".join(value[:2])
    regex = re.compile('[^0-9.]')
    return regex.sub('', value)


def remove_nonascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


filepath = '/Users/abhishek/Desktop/olx/99acres/links/bangalore-2.json'
links = json.loads(open(filepath).read())

data_list = []
start = 9000
end = 18200

for index, link in enumerate(links[start:end]):
    link = link.split('?')
    if link:
        link = link[0]
    else:
        continue
    print index, len(links)
    try:
        browser.get(link)
    except:
        continue

    try:
        browser.execute_script("window.scrollTo(0, 10000000)")
    except:
        pass

    try:
        myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#amenitiesSection > div > div:nth-child(2) > div.xidBasicAmn > div:nth-child(2)')))
    except TimeoutException:
        pass

    try:
        browser.execute_script('xid99.loadMap();')
    except:
        pass

    try:
        browser.execute_script("window.scrollTo(0, 0)")
    except:
        pass

    try:
        myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="locHighlightsSlide"]')))
    except TimeoutException:
        pass

    data = dict()
    try:
        data['Project_Name'] = browser.find_element_by_css_selector(
            "#xid_GalTxt > h1 > div > div.project-name").text
    except:
        pass

    data['Operation_Type'] = 'Project Add'

    try:
        city = browser.find_element_by_css_selector(
            "#xidPages > div.contentWrap.xid_DetailPage > div.xid_basicDetailWrap1.contentInnerWrap.xid_tb0 > div > div > div > span:nth-child(2) > a > span").text
        data['City'] = city[12:]
    except:
        pass

    try:
        breadcrum = list(browser.find_elements_by_css_selector('#xidPages > div.xid_DetailPage > div.xid_basicDetailWrap1 > div > div > div > span'))
    except:
        breadcrum = []

    data['Address'] = remove_nonascii(", ".join([a.text for a in breadcrum[2:-1]]))

    try:
        data['Display_Locality'] = browser.find_element_by_css_selector('#xid_GalTxt > h1 > div > div.project-location > span').text
    except Exception as e:
        data['Display_Locality'] = ''

    try:
        unit_details = browser.find_elements_by_css_selector('.fpcRow')
    except:
        unit_details = []

    try:
        browser.find_element_by_css_selector('#xidSpecific > a.dev_specificLessMore').click()
    except:
        pass
    try:
        data['Specifications'] = browser.find_element_by_css_selector('#specificationsSection > div').text
    except:
        data['Specifications'] = ''

    bank_approvals = []
    try:
        bank_approvals_ele = browser.find_elements_by_css_selector('.bankBodr')
    except:
        bank_approvals_ele = []
    for bank_approval in bank_approvals_ele:
        try:
            bank_approvals.append(bank_approval.find_element_by_tag_name('img').get_attribute('title'))
        except:
            pass
    data['Loan_Approvals'] = ','.join(bank_approvals)

    try:
        amenities = []
        amenities_ele = browser.find_element_by_css_selector(
            '#amenitiesSection > div > div:nth-child(2) > div.xidBasicAmn > div:nth-child(2)').find_elements_by_tag_name('div')
        for amenity in amenities_ele:
            amenities.append(amenity.text)
        amenities = list(set(amenities))
        amenities = [a for a in amenities if 'no' != a.lower()[:2]]
        data['Amenities'] = ','.join(amenities)
    except Exception as e:
        data['Amenities'] = ''

    try:
        data['Lat'] = browser.find_element_by_xpath('//*[@id="mapSection"]/span/span/meta[1]').get_attribute('content')
        data['Lon'] = browser.find_element_by_xpath('//*[@id="mapSection"]/span/span/meta[2]').get_attribute('content')
    except:
        data['Lat'] = ''
        data['Lon'] = ''

    construction_status = ''
    try:
        boxes = browser.find_element_by_css_selector('#xidFactTable').find_elements_by_tag_name('div')
    except:
        boxes = []
    data['Construction_Status'] = ''
    data['Prices_Min'] = ''
    data['Prices_Max'] = ''
    data['Property_Types'] = ''
    for a in boxes:
        try:
            label = a.find_element_by_css_selector('.factLbl').text.lower()
        except Exception as e:
            label = ''
        if 'possession' in label:
            try:
                data['Construction_Status'] = a.find_element_by_css_selector('.factVal1').text
            except:
                data['Construction_Status'] = ''
            try:
                data['Possession_Date'] = a.find_element_by_css_selector('.factVal2').text
            except:
                data['Possession_Date'] = ''

            data['Possession_Date'] = re.sub('Completed in', '', data['Possession_Date'])
        elif 'configuration' in label:
            try:
                p_type = a.find_element_by_css_selector('.factVal1').text.lower()
                if p_type in ['apartment', 'villa', 'row house', 'builder floor', 'plot', 'studio', 'land']:
                    data['Property_Types'] = p_type
                else:
                    data['Property_Types'] = ''
            except:
                pass
        elif 'base price' in label:
            try:
                price_range = a.find_element_by_css_selector('.factValsecond').text.split('to')

                if 'lac' in price_range[1].strip().lower():
                    data['Prices_Max'] = only_decimal(price_range[1].strip()) + " Lac"
                elif 'crore' in price_range[1].strip().lower():
                    data['Prices_Max'] = only_decimal(price_range[1].strip()) + " Crore"
                else:
                    data['Prices_Max'] = only_decimal(price_range[1].strip()) + " Lac" if float(
                        only_decimal(price_range[1].strip())) > 10.0 else only_decimal(price_range[1].strip()) + " Crore"

                if 'lac' in price_range[0].strip().lower():
                    data['Prices_Min'] = only_decimal(price_range[0].strip()) + " Lac"
                elif 'crore' in price_range[0].strip().lower():
                    data['Prices_Min'] = only_decimal(price_range[0].strip()) + " Crore"
                else:
                    data['Prices_Min'] = only_decimal(price_range[0].strip()) + " Lac" if float(
                        only_decimal(price_range[0].strip())) > 10.0 else only_decimal(price_range[0].strip()) + " Crore"
            except Exception as e:
                pass

    try:
        data['Highlights'] = browser.find_element_by_xpath('//*[@id="locHighlightsSlide"]').text
    except Exception as e:
        data['Highlights'] = ''
    try:
        data['Description'] = browser.find_element_by_xpath('//*[@id="item_desc"]').text
    except:
        data['Description'] = ''
    try:
        data['RERA_Registration_Number'] = browser.find_element_by_css_selector(
            '#overviewSection > div > table > tbody > tr > td > div > div.npReraText > span > a').get_attribute('title')
    except Exception as e:
        try:
            data['RERA_Registration_Number'] = browser.find_element_by_css_selector(
                '#overviewSection > div > table > tbody > tr > td > div > div.npReraText > span > span').get_attribute(
                'title')
        except:
            pass
    try:
        data['Builder'] = browser.find_element_by_css_selector('#item_manufacturer').text
    except:
        pass

    BHKs = []

    data['Number_Of_Units'] = ''
    data['Open_Area_Percentage'] = ''
    data['Size'] = ''
    data['Total_Number_Of_Floors'] = ''
    try:
        number_unit_eles = browser.find_element_by_css_selector(
            '#overviewSection > div > div.projFacts.secFactWrap').find_elements_by_tag_name('div')
    except:
        number_unit_eles = []
    for a in number_unit_eles:
        if 'units' in a.text.lower():
            data['Number_Of_Units'] = only_number(a.text)
        elif 'open' in a.text.lower():
            data['Open_Area_Percentage'] = only_number(a.text)
        elif 'project area' in a.text.lower():
            data['Size'] = only_decimal(a.text)
            if a and len(a.text.split(":")) > 1:
                data['Size_Unit'] = only_char(a.text.split(":")[1])
            else:
                data['Size_Unit'] = ''
        elif 'floor' in a.text.lower():
            data['Total_Number_Of_Floors'] = only_number(a.text)
        elif 'tower' in a.text.lower():
            data['Total_Number_Of_Towers'] = only_number(a.text)

    # Photos
    try:
        browser.execute_script("$('#x_viewAllPhotos').click()")
    except:
        pass

    unit_number_of_units = {}
    for a in unit_details:
        n = a.get_attribute('data-property-type')
        if n in unit_number_of_units:
            unit_number_of_units[n] += 1
        else:
            unit_number_of_units[n] = 1

    min_sbua = ''
    max_sbua = ''
    for i in range(len(unit_details)):
        sub_data = {
            'Project_Name': data['Project_Name'],
            'City': data['City'] if 'City' in data else ''
        }
        sub_data['Unit_Number_Of_Units'] = unit_number_of_units[unit_details[i].get_attribute('data-property-type')]
        sub_data['Unit_ID'] = i+1
        try:
            unit_name = browser.execute_script(
                "return $('#unitDetContainer > div:nth-child(%s)').attr('data-property-type')" % (i + 2))

            if 'bhk' in unit_name.lower():
                sub_data['Unit_Name'] = unit_name[:5]
            else:
                sub_data['Unit_Name'] = unit_name

        except Exception as e:
            sub_data['Unit_Name'] = ''
            unit_name = ''

        if sub_data['Unit_Name']:
            BHKs.append(only_number(sub_data['Unit_Name']))

        sub_data['Unit_Property_Types'] = ''
        for a in ['apartment', 'villa', 'row houses', 'builder floor', 'plot', 'studio']:
            if re.search(a, unit_name, re.IGNORECASE):
                sub_data['Unit_Property_Types'] = a
                break
        try:
            qaInclusions = browser.execute_script('return $("#unitDetContainer > div:nth-child(%s) > div.qaInclusions").text()' % (i + 2))
        except Exception as e:
            qaInclusions = ''

        sub_data['Unit_Bedrooms'] = ''
        sub_data['Unit_Bathrooms'] = ''
        sub_data['Unit_Balcony'] = ''
        qaInclusions = qaInclusions.lower()
        if 'bedroom' in qaInclusions:
            sub_data['Unit_Bedrooms'] = qaInclusions[qaInclusions.index('bedroom') - 2: qaInclusions.index('bedroom')]
        if 'bathroom' in qaInclusions:
            sub_data['Unit_Bathrooms'] = qaInclusions[qaInclusions.index('bathroom') - 2: qaInclusions.index('bathroom')]
        if 'balcony' in qaInclusions:
            sub_data['Unit_Balcony'] = qaInclusions[qaInclusions.index('balcony') - 2: qaInclusions.index('balcony')]

        try:
            rows = len(browser.find_element_by_css_selector('#unitDetContainer > div:nth-child(%s) > div.fpcColumn.flt.qaAreaDiv' % (i + 2)).find_elements_by_tag_name('div'))
        except:
            rows = 0

        for r in range(rows):
            try:
                qaAreaDiv = browser.execute_script('return $("#unitDetContainer > div:nth-child(%s) > div.qaAreaDiv > div:nth-child(%s)").text()' % (i + 2, r + 1))
            except Exception as e:
                qaAreaDiv = ''

            qaAreaDiv = qaAreaDiv.lower()
            qaAreaDiv = " ".join(qaAreaDiv.split())

            a = qaAreaDiv.lower()
            if not a.strip():
                continue
            area = a.split('sq')
            if 'carpet' in a:
                sub_data['Unit_Carpet_Area'] = only_decimal(area[0]) if area else ''
            if 'plot' in a:
                sub_data['Unit_Carpet_Area'] = only_decimal(area[0]) if area else ''
            elif 'super built-up' in a:
                sub_data['Unit_Super_Builtup_Area'] = only_decimal(area[0]) if area else ''
                if sub_data['Unit_Super_Builtup_Area'] > max_sbua or not max_sbua:
                    max_sbua = sub_data['Unit_Super_Builtup_Area']
                if sub_data['Unit_Super_Builtup_Area'] < min_sbua or not min_sbua:
                    min_sbua = sub_data['Unit_Super_Builtup_Area']
            elif 'built-up' in a:
                sub_data['Unit_Builtup_Area'] = only_decimal(area[0]) if area else ''
            sub_data['Area_Unit'] = only_char(a.split(':')[1].replace('.', ' ')).strip() if len(a.split(':')) > 1 else ''
            if 'me' in sub_data['Area_Unit'].lower():
                sub_data['Area_Unit'] = 'sq meter'
            elif 'f' in sub_data['Area_Unit'].lower() and 't' in sub_data['Area_Unit'].lower():
                sub_data['Area_Unit'] = 'sq ft'
            data['Super_Built_Up_Area_Min'] = min_sbua
            data['Super_Built_Up_Area_Max'] = max_sbua
        try:
            prices = browser.execute_script(
                'return $("#unitDetContainer > div:nth-child(%s) > div.fpcColumn.qaNewBookingPriceDiv").text()' % (
                i + 2))
        except Exception as e:
            prices = ''
        prices = prices.split('-')
        # print prices
        try:
            if 'lac' in prices[0].strip().lower():
                sub_data['Unit_Price_Min'] = only_decimal(prices[0].strip()) + " Lac"
            elif 'crore' in prices[0].strip().lower():
                sub_data['Unit_Price_Min'] = only_decimal(prices[0].strip()) + " Crore"
            else:
                sub_data['Unit_Price_Min'] = only_decimal(prices[0].strip()) + " Lac" if float(only_decimal(prices[0].strip())) > 10.0 else only_decimal(prices[0].strip()) + " Crore"

        except Exception as e:
            pass
        try:
            if 'lac' in prices[1].strip().lower():
                sub_data['Unit_Price_Max'] = only_decimal(prices[1].strip()) + " Lac"
            elif 'crore' in prices[1].strip().lower():
                sub_data['Unit_Price_Max'] = only_decimal(prices[1].strip()) + " Crore"
            else:
                sub_data['Unit_Price_Max'] = only_decimal(prices[1].strip()) + " Lac" if float(only_decimal(prices[1].strip())) > 10.0 else only_decimal(prices[1].strip()) + " Crore"
        except:
            pass

        sub_data['Operation_Type'] = 'Unit Add'
        data_list.append(sub_data)

    images = []
    try:
        myElem = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#photonXid > div.slideBar > div.rel.thumbsWrpr > div.filmStrip > ul')))
    except TimeoutException:
        pass

    try:
        image_length = range(len(browser.find_element_by_css_selector(
            '#photonXid > div.slideBar > div.rel.thumbsWrpr > div.filmStrip > ul').find_elements_by_tag_name('li')))
    except:
        image_length = []

    for i in image_length:
        try:
            images.append(browser.execute_script(
                "return $('#photonXid > div.slideBar > div.rel.thumbsWrpr > div.filmStrip > ul > li:nth-child(%s) > img').attr('data')" % (
                        i + 1)))
        except Exception as e:
            pass
    for image in images:
        sub_data = dict({
            'Image_Folder': image,
            'Project_Name': data['Project_Name'],
            'City': data['City'] if 'City' in data else ''
        })
        sub_data['Operation_Type'] = 'Image Add'
        data_list.append(sub_data)

    data['BHKs'] = ','.join(sorted(list(set(BHKs))))
    data_list.append(data)
    try:
        browser.execute_script("$('#photonXid > div.photonCrossWrap').click()")
    except:
        pass

df = pd.DataFrame(data_list)
df.to_csv('/Users/abhishek/Desktop/olx/99acres/data/bangalore%s-%s.csv' % (str(start), str(end)), encoding='utf-8')
