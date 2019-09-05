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
import json
import requests, os

browser = webdriver.Chrome("/Users/abhishek/chromedriver")


def only_number(value):
    regex = re.compile('[^0-9]')
    return regex.sub('', value)


def only_char(value):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', value)


def remove_nonascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def only_decimal(value):
    regex = re.compile('[^0-9.]')
    return regex.sub('', value)


filepath = '/Users/abhishek/Desktop/olx/proptiger/links/chennai.json'
links = json.loads(open(filepath).read())

start = 4100
end = 5000

data_list = []
for index, link in enumerate(links[start: end]):
    print index, len(links)
    link = "https://www.proptiger.com" + link
    try:
        browser.get(link)
    except:
        continue

    try:
        browser.execute_script("window.scrollTo(0, 10000000)")
    except:
        pass

    # try:
    #     browser.execute_script('xid99.loadMap();')
    # except:
    #     pass

    try:
        myElem = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#amenities > div > div > a')))
    except TimeoutException:
        pass

    try:
        browser.execute_script("window.scrollTo(0, 0)")
    except:
        pass

    try:
        myElem = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#specifications > div > a')))
    except TimeoutException:
        pass

    try:
        summary = browser.find_element_by_css_selector('#projectDetailsPageWrapperFull')
    except:
        pass

    data = dict()
    try:
        data['Project_Name'] = browser.find_element_by_css_selector('#projectDetailsPageWrapperFull > div:nth-child(5) > div.left-col.va-top > section.project-main-name > div > div > h1 > div.title-name').text
    except:
        data['Project_Name'] = ''

    try:
        data['Builder'] = summary.get_attribute('data-builder')
    except:
        pass

    data['Operation_Type'] = 'Project Add'

    try:
        browser.execute_script('$("#amenities > div > div > a").click()')
    except Exception as e:
        pass

    try:
        browser.execute_script('$("#specifications > div.more-link-wrap > a").click()')
    except Exception as e:
        pass

    try:
        browser.execute_script('$("#overview > div.project-desc-wrap > p.proj-desc.short-desc > span").click()')
    except Exception as e:
        pass


    try:
        data['City'] = summary.get_attribute('data-cityname')
    except:
        data['City'] = ''

    try:
        data['Display_Locality'] = summary.get_attribute('data-localitylabel') + " " + summary.get_attribute('data-cityname')
    except Exception as e:
        data['Display_Locality'] = ''

    data['Specifications'] = []
    try:
        specification = browser.find_element_by_css_selector('#specifications div.spec-types')
        for i in specification.find_elements_by_css_selector('div.spec-row'):
            data['Specifications'].append(i.text)
    except:
        pass
    data['Specifications'] = ','.join(data['Specifications'])

    bank_approvals = []
    try:
        bank_approvals_ele = browser.find_element_by_css_selector(
            '#overview > div.app-banks > ul').find_elements_by_tag_name('li')
    except Exception as e:
        bank_approvals_ele = []
    for bank_approval in bank_approvals_ele:
        name = None
        try:
            name = bank_approval.find_element_by_tag_name('img').get_attribute('alt')
            if '(' in name:
                name = name.split('(')[0]
        except:
            name = bank_approval.text
        bank_approvals.append(name)
    data['Loan_Approvals'] = ','.join(bank_approvals)

    try:
        amenities = []
        amenities_ele = browser.find_element_by_css_selector(
            '#amenities > div > ul').find_elements_by_tag_name('li')
        for amenity in amenities_ele:
            amenities.append(amenity.text)
        amenities = list(set(amenities))
        data['Amenities'] = ','.join(amenities)
    except Exception as e:
        data['Amenities'] = ''

    try:
        data['Address'] = browser.find_element_by_css_selector('#projectDetailsPageWrapperFull  div.location-wrap > span > a').text
    except Exception as e:
        data['Address'] = ''

    try:
        data['Lat'] = summary.get_attribute('data-lat')
        data['Lon'] = summary.get_attribute('data-long')
    except:
        data['Lat'] = ''
        data['Lon'] = ''

    try:
        p_type = summary.get_attribute('data-unittype').lower()
    except:
        p_type = ''

    if p_type in ['apartment', 'villa', 'row house', 'builder floor', 'plot', 'studio']:
        data['Property_Types'] = p_type
    else:
        data['Property_Types'] = ''

    try:
        data['Construction_Status'] = summary.get_attribute('data-projectstatus')
    except:
        data['Construction_Status'] = ''

    construction_status = ''
    try:
        boxes = browser.find_element_by_css_selector('#overview > ul').find_elements_by_tag_name('li')
    except:
        boxes = []
    for a in boxes:
        try:
            label = a.find_element_by_css_selector('div.overview-label').text.lower()
        except Exception as e:
            label = ''
        try:
            value = a.find_element_by_css_selector('div.overview-value').text
        except:
            value = ''
        if 'possession' in label:
            try:
                data['Possession_Date'] = value
            except:
                data['Possession_Date'] = ''
        elif 'area' in label:
            try:
                data['Size'] = only_number(value)
            except:
                data['Size'] = ''
            try:
                data['Size_Unit'] = only_char(value)
            except:
                data['Size_Unit'] = ''
        elif 'apartments' in label:
            try:
                data['Number_Of_Units'] = value
            except:
                data['Number_Of_Units'] = ''
        elif 'launch' in label:
            try:
                data['Launch_Date'] = value
            except:
                data['Launch_Date'] = ''

    data['Highlights'] = []
    try:
        highlights = browser.find_element_by_css_selector('#neighbourhood > div > ul').find_elements_by_tag_name('li')
        for h in highlights:
            data['Highlights'].append(h.text)
    except Exception as e:
        pass
    data['Highlights'] = ','.join(data['Highlights'])

    try:
        data['Last_Updated_On'] = browser.find_element_by_css_selector('#projectDetailsPageWrapperFull > div:nth-child(2) > div.breadcrumb-wrap > div.page-last-updated > span > span').text
    except:
        pass

    try:
        data['Description'] = browser.find_element_by_css_selector('#overview > div.project-desc-wrap > p.proj-desc.full-desc.js-long-overview-link').text
    except Exception as e:
        data['Description'] = ''
    try:
        data['RERA_Registration_Number'] = browser.find_element_by_css_selector('span.rera-value').text
    except Exception as e:
        data['RERA_Registration_Number'] = ''

    try:
        data['Prices_Min'] = summary.get_attribute('data-budgetlowerlimit')
        data['Prices_Max'] = summary.get_attribute('data-budgetupperlimit')
    except:
        pass

    try:
        number_unit_eles = browser.find_element_by_css_selector(
            '#projectDetailsPageWrapperFull div.project-spec-wrap').find_elements_by_css_selector(
            'div.spec-section')
    except Exception as e:
        number_unit_eles = []
    for b in number_unit_eles:
        try:
            number_unit_eles2 = b.find_elements_by_css_selector('div.project-spec')
        except Exception as e:
            continue
        for a in number_unit_eles2:
            try:
                label = ''.join([i.text for i in a.find_elements_by_css_selector('.spec-label')]).lower()
            except Exception as e:
                continue
            if 'builtup' in label:
                try:
                    data['Super_Builtup_Area_Min'] = only_decimal(
                        a.find_element_by_css_selector('div.spec-value > div > span.first-val').text)
                except Exception as e:
                    pass
                try:
                    data['Super_Builtup_Area_Max'] = only_decimal(
                        a.find_element_by_css_selector('div.spec-value > div > span.second-val').text)
                except:
                    pass
                try:
                    data['Area_Unit'] = a.find_element_by_css_selector('div.spec-value > div > span.trail-label').text
                except:
                    pass
            elif 'carpet' in label:
                try:
                    data['Carpet_Area_Min'] = only_decimal(
                        a.find_element_by_css_selector('div.spec-value > div > span.first-val').text)
                except Exception as e:
                    pass
                try:
                    data['Carpet_Area_Max'] = only_decimal(
                        a.find_element_by_css_selector('div.spec-value > div > span.second-val').text)
                except Exception as e:
                    pass
                try:
                    data['Area_Unit'] = a.find_element_by_css_selector('div.spec-value > div > span.trail-label').text
                except:
                    pass
            elif 'area' in label:
                try:
                    data['Carpet_Area_Min'] = only_decimal(
                        a.find_element_by_css_selector('div.spec-value > div > span.first-val').text)
                except:
                    pass
                try:
                    data['Carpet_Area_Max'] = only_decimal(
                        a.find_element_by_css_selector('div.spec-value > div > span.second-val').text)
                except:
                    pass
                try:
                    data['Area_Unit'] = a.find_element_by_css_selector('div.spec-value > div > span.trail-label').text
                except:
                    pass
            if 'apartment' in label or 'villa' in label:
                try:
                    data['BHKs'] = ",".join(
                        [a for a in only_number(a.find_element_by_css_selector('div.spec-value').text)])
                except:
                    pass

    try:
        units = browser.find_element_by_css_selector('#floorplan > div.config-wrap').find_elements_by_css_selector(
            'div.config-table-wrap')
    except:
        units = []
    for a in range(len(units)):
        try:
            browser.execute_script(
                '$("#floorplan > div.config-wrap > div.config-table-wrap:nth-child(%s)").removeClass("hide")' % (a + 2))
        except:
            pass
        try:
            browser.execute_script(
                '$("#floorplan > div.config-wrap > div.config-table-wrap:nth-child(%s)").addClass("show-all")' % (
                    a + 2))
        except:
            pass

    try:
        units = browser.find_element_by_css_selector('#floorplan > div.config-wrap').find_elements_by_tag_name('tr')
    except:
        units = []

    last_unit_count = 1
    carpet_area = None
    builtup_area = None
    price = None
    min_carpet_area = None
    max_carpet_area = None
    max_builtup_area = None
    min_builtup_area = None
    for i, unit in enumerate(units):
        sub_data = {
            'Project_Name': data['Project_Name'],
            'City': data['City'],
        }
        if 'bot-border' in unit.get_attribute('class'):
            tds = unit.find_elements_by_tag_name('th')
            for i, td in enumerate(tds):
                if 'total area' in td.text.lower():
                    builtup_area = i
                elif 'carpet area' in td.text.lower():
                    carpet_area = i
                elif 'area' == td.text.lower():
                    carpet_area = i
                if 'price' in td.text.lower():
                    price = i
                    break
            continue
        else:
            if carpet_area is not None:
                try:
                    td = unit.find_element_by_css_selector('td:nth-child(%s)' % (carpet_area + 1))
                except Exception as e:
                    continue
                try:
                    unit_name = td.find_element_by_css_selector('div.unit-size-label').text
                except Exception as e:
                    unit_name = ''
                unit_name = re.sub('[()]', '', unit_name)
                sub_data['Unit_Name'] = unit_name

                try:
                    sub_data['Unit_Carpet_Area'] = only_number(td.find_element_by_tag_name('a').text)
                    if min_carpet_area > sub_data['Unit_Carpet_Area'] or not min_carpet_area:
                        min_carpet_area = sub_data['Unit_Carpet_Area']
                    if max_carpet_area < sub_data['Unit_Carpet_Area'] or not max_carpet_area:
                        max_carpet_area = sub_data['Unit_Carpet_Area']
                    sub_data['Unit_Area_Unit'] = only_char(td.find_element_by_tag_name('a').text)
                except:
                    pass

                unit_names = unit_name.split('+')
                for u in unit_names:
                    if 'bhk' in u.lower():
                        sub_data['Unit_Bedroom'] = u[0]
                    elif 't' in u.lower():
                        sub_data['Unit_Bathroom'] = u[0]

            if builtup_area is not None:
                try:
                    td = unit.find_element_by_css_selector('td:nth-child(%s)' % (builtup_area + 1))
                    sub_data['Unit_Builtup_Area'] = only_number(td.text)
                    if min_builtup_area > sub_data['Unit_Builtup_Area'] or not min_builtup_area:
                        min_builtup_area = sub_data['Unit_Builtup_Area']
                    if max_builtup_area < sub_data['Unit_Builtup_Area'] or not max_builtup_area:
                        max_builtup_area = sub_data['Unit_Builtup_Area']
                    sub_data['Unit_Area_Unit'] = only_char(td.text)
                except Exception as e:
                    pass

            if price is not None:
                try:
                    td = unit.find_element_by_css_selector('td:nth-child(%s)' % (price + 1))
                    sub_data['Unit_Price'] = remove_nonascii(td.text)
                except Exception as e:
                    pass

        sub_data['Unit_Id'] = last_unit_count
        last_unit_count += 1
        sub_data['Operation_Type'] = 'Unit Add'
        data_list.append(sub_data)

    data['Super_Builtup_Area_Max'] = max_builtup_area if 'Super_Builtup_Area_Max' not in data else 0
    data['Super_Builtup_Area_Min'] = min_builtup_area if 'Super_Builtup_Area_Min' not in data else 0
    data['Carpet_Area_Max'] = max_carpet_area if 'Carpet_Area_Max' not in data else data['Carpet_Area_Max']
    data['Carpet_Area_Min'] = min_carpet_area if 'Carpet_Area_Min' not in data else data['Carpet_Area_Min']
    try:
        image_url = 'https://www.proptiger.com/xhr/project/%s/images?format=json' % summary.get_attribute(
            'data-projectid')
        images = requests.get(url=image_url, headers={"content-type": "application/json; charset=UTF-8"}).json()
        for i in images:
            sub_data = dict({
                'Project_Name': data['Project_Name'],
                'City': data['City'],
                'Image_Folder': i['absolutePath'],
            })
            sub_data['Operation_Type'] = 'Image Add'
            data_list.append(sub_data)
    except Exception as e:
        pass

    data_list.append(data)

df = pd.DataFrame(data_list)
df.to_csv('/Users/abhishek/Desktop/olx/proptiger/data/chennai%s-%s.csv' % (start, end), encoding='utf-8')
