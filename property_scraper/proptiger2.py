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


def only_decimal(value):
    regex = re.compile('[^0-9.]')
    return regex.sub('', value)


path = '/Users/abhishek/Desktop/olx/proptiger/links2'
for filename in os.listdir(path):
    if not filename.endswith(".json"):
        continue
    filepath = os.path.join(path, filename)
    links = json.loads(open(filepath).read())

    data_list = []
    for index, link in enumerate(links):
        print index, len(links), filename
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
            data['Project_Name'] = summary.get_attribute('data-projectname')
        except:
            pass

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
            browser.execute_script('$("#overview > div.project-desc-wrap > p.proj-desc.short-desc.js-more-less-parent.js-short-overview-link > span").click()')
        except Exception as e:
            pass


        try:
            data['City'] = summary.get_attribute('data-cityname')
        except:
            data['City'] = ''

        try:
            data['Display_Locality'] = summary.get_attribute('data-localitylabel')
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
                '#overview > div.app-banks > ul').find_elements_by_tag_name('img')
        except Exception as e:
            # print e
            bank_approvals_ele = []
        for bank_approval in bank_approvals_ele:
            name = bank_approval.get_attribute('alt')
            if '(' in name:
                name = name.split('(')[0]
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
            # print e
            data['Amenities'] = ''

        try:
            data['Address'] = browser.find_element_by_css_selector('#projectDetailsPageWrapperFull  div.location-wrap > span > a').text
        except Exception as e:
            # print e
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
                    data['Size'] = only_decimal(value)
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
            # print e
            data['Description'] = ''
        try:
            data['RERA_Registration_Number'] = browser.find_element_by_css_selector('#projectDetailsPageWrapperFull div.details-wrap  div.rera-wrap  span.rera-value').text
        except Exception as e:
            # print e
            data['RERA_Registration_Number'] = ''

        try:
            data['Prices_Min'] = summary.get_attribute('data-budgetlowerlimit')
            data['Prices_Max'] = summary.get_attribute('data-budgetupperlimit')
        except:
            pass

        try:
            number_unit_eles = browser.find_element_by_css_selector(
                '#projectDetailsPageWrapperFull > div:nth-child(2) > div.left-col > section.project-title-section > div > div.project-spec-wrap').find_elements_by_tag_name(
                'div.spec-section')
        except:
            number_unit_eles = []
        for a in number_unit_eles:
            label = a.find_element_by_css_selector('div.spec-label').lower()
            if 'builtup' in a.text.lower():
                data['Super_Builtup_Area_Min'] = only_decimal(
                    a.find_element_by_css_selector('div.spec-value > div > span.first-val').text)
                data['Super_Builtup_Area_Max'] = only_decimal(
                    a.find_element_by_css_selector('div.spec-value > div > span.second-val').text)
                data['Area_Unit'] = a.find_element_by_css_selector('div.spec-value > div > span.trail-label')
            elif 'apartment' in a.text.lower():
                data['BHKs'] = ",".join([a for a in only_number(a.find_element_by_css_selector('div.spec-value').text)])


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
        for unit in units:
            sub_data = {}
            try:
                td = unit.find_element_by_css_selector('td:nth-child(2)')
            except:
                continue
            try:
                unit_name = td.find_element_by_css_selector('div.unit-size-label').text
            except:
                unit_name = ''
            unit_name = re.sub('[()]', '', unit_name)
            try:
                sub_data['Unit_Name'] = unit_name
            except:
                pass
            try:
                sub_data['Unit_Carpet_Area'] = only_number(td.find_element_by_tag_name('a').text)
                sub_data['Unit_Area_Unit'] = only_char(td.find_element_by_tag_name('a').text)
            except:
                pass
            unit_names = unit_name.split('+')
            for u in unit_names:
                if 'bhk' in u.lower():
                    sub_data['Unit_Bedroom'] = u[0]
                elif 't' in u.lower():
                    sub_data['Unit_Bathroom'] = u[0]

            sub_data.update(data)
            sub_data['Operation_Type'] = 'Unit Add'
            data_list.append(sub_data)

        try:
            image_url = 'https://www.proptiger.com/xhr/project/%s/images?format=json' % summary.get_attribute(
                'data-projectid')
            images = requests.get(url=image_url, headers={"content-type": "application/json; charset=UTF-8"}).json()
            for i in images:
                sub_data = {
                    'Image_Folder': i['absolutePath'],
                }
                sub_data.update(data)
                sub_data['Operation_Type'] = 'Image Add'
                data_list.append(sub_data)
        except Exception as e:
            pass

        data_list.append(data)

    df = pd.DataFrame(data_list)
    df.to_csv('/Users/abhishek/Desktop/olx/proptiger/data/%s.csv' % filename, encoding='utf-8')
