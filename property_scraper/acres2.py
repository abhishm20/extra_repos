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
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', value)


def only_decimal(value):
    regex = re.compile('[^0-9.]')
    return regex.sub('', value)


path = '/Users/abhishek/Desktop/olx/99acres/links2/'
for filename in os.listdir(path)[:1]:
    filename = 'ahmedabad-2.json'
    if not filename.endswith(".json"):
        continue
    filepath = os.path.join(path, filename)
    links = json.loads(open(filepath).read())

    data_list = []
    start = 1000
    end = 2000
    for index, link in enumerate(links[start:end]):
        print index, len(links), filename
        try:
            browser.get(link)
        except:
            continue

        try:
            browser.execute_script("window.scrollTo(0, 10000000)")
        except:
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
            myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#amenitiesSection > div > div:nth-child(2) > div.xidBasicAmn > div:nth-child(2)')))
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
            spans = browser.find_element_by_css_selector(
                '#xidPages > div.contentWrap.xid_DetailPage > div.xid_basicDetailWrap1.contentInnerWrap.xid_tb0 > div > div > div').find_elements_by_tag_name(
                'span')
            data['Display_Locality'] = spans[-3].text
        except Exception as e:
            data['Display_Locality'] = ''

        try:
            unit_details = browser.find_elements_by_css_selector('.fpcRow')
        except:
            unit_details = []

        data['Number_Of_Units'] = len(unit_details)

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
                '#amenitiesSection > div > div:nth-child(2) > div.xidBasicAmn.floatl > div:nth-child(2)').find_elements_by_tag_name('div')
            for amenity in amenities_ele:
                amenities.append(amenity.text)
            amenities = list(set(amenities))
            data['Amenities'] = ','.join(amenities)
        except Exception as e:
            data['Amenities'] = ''

        try:
            address = browser.find_element_by_xpath('//*[@id="xMapSec"]/div/h4').text
        except:
            address = ''
        data['Address'] = ''
        if 'Map' in address:
            data['Address'] = re.sub('map', '', address, flags=re.IGNORECASE)

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
                    if p_type in ['apartment', 'villa', 'row house', 'builder floor', 'plot', 'studio']:
                        data['Property_Types'] = p_type
                    else:
                        data['Property_Types'] = ''
                except:
                    pass
            elif 'base price' in label:
                try:
                    price_range = a.find_element_by_css_selector('.factValsecond').text.split('to')
                    data['Prices_Min'] = only_decimal(price_range[0])
                    data['Prices_Max'] = only_decimal(price_range[1])
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
            data['RERA_Registration_Number'] = browser.find_element_by_xpath(
                '//*[@id="overviewSection"]/div/table/tbody/tr/td/div/div[3]/span/a').text
            rera_split = data['RERA_Registration_Number'].split(':')
            if len(rera_split) > 1:
                data['RERA_Registration_Number'] = rera_split[1]
        except:
            pass
        try:
            data['Builder'] = browser.find_element_by_css_selector('#item_manufacturer').text
        except:
            pass

        BHKs = []

        data['Unit_Number_Of_Units'] = ''
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
                data['Unit_Number_Of_Units'] = only_number(a.text)
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

        for i in range(len(unit_details)):
            sub_data = {}
            sub_data['Unit_ID'] = i+1
            try:
                unit_name = browser.execute_script(
                    "return $('#unitDetContainer > div:nth-child(%s)').attr('data-property-type')" % (i + 2))
                sub_data['Unit_Name'] = unit_name[:5]
            except Exception as e:
                sub_data['Unit_Name'] = ''
                unit_name = ''

            if sub_data['Unit_Name']:
                BHKs.append(sub_data['Unit_Name'])

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
                rows = len(browser.find_element_by_css_selector('#optionId_864557_23037 > div.fpcColumn.width30per.flt.qaAreaDiv').find_elements_by_tag_name('div'))
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
                area = re.findall("\d+\.\d+", a)
                if 'carpet' in a:
                    sub_data['Unit_Carpet_Area'] = area[0] if area else ''
                elif 'super built-up' in a:
                    sub_data['Unit_Super_Builtup_Area'] = area[0] if area else ''
                sub_data['Area_Unit'] = 'sqft'
            sub_data.update(data)
            sub_data['Operation_Type'] = 'Unit Add'
            data_list.append(sub_data)

        images = []
        try:
            myElem = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#photonXid > div.slideBar > div.rel.thumbsWrpr > div.filmStrip > ul')))
        except TimeoutException:
            print "Image loading took too much time!"

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
                print "Images", e
        for image in images:
            sub_data = {
                'Image_Folder': image,
            }
            sub_data.update(data)
            sub_data['Operation_Type'] = 'Image Add'
            data_list.append(sub_data)

        data['BHKs'] = ','.join(BHKs)
        data_list.append(data)
        try:
            browser.execute_script("$('#photonXid > div.photonCrossWrap').click()")
        except:
            pass

    df = pd.DataFrame(data_list)
    df.to_csv('/Users/abhishek/Desktop/olx/99acres/data/%s (%s-%s).csv' % (filename, start, end), encoding='utf-8')
