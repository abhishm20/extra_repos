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


dir = '/Users/abhishek/Desktop/olx/sbi-2/links'
base_dir = '/Users/abhishek/Desktop/olx/sbi-2/images/'
today = "2018-06-29"


filepath = '/Users/abhishek/Desktop/olx/sbi-2/links/Noida.json'
file_data = open(filepath, 'r+')
data_list = json.loads(file_data.read())
list_data = []
for s,a in enumerate(data_list[:200]):
    print s, len(data_list)
    row = {}
    data = json.loads(json.loads(a['d'])[0])[0]
    row['Project_Name'] = data['ProjectName']
    row['Operation_Type'] = 'Project Add'
    row['City'] = data['CityName']

    row['Address'] = data['ColonyDesc'] + ', ' + data['CityName']
    row['Display_Locality'] = data['ColonyDesc'] + ', ' + data['CityName']
    row['Lat'] = data['Lat']
    row['Lon'] = data['Lon']
    row['Size_Unit'] = 'Acres'
    row['Launch_Date'] = data['LaunchDate']
    row['Possession_Date'] = data['CompletionDate']
    row['Available_Construction_Status'] = data['CurrentStatus']
    if data['CurrentStatus'].lower() in ["new launch", "under construction", "ready to move"]:
        row['Construction_Status'] = data['CurrentStatus']
    row['Total_Number_Of_Floors'] = data['NumberOfFloors']
    row['Total_Number_Of_Blocks'] = data['NoOfTowers']
    row['Builder'] = data['BuilderDesc']
    row['Area_Unit'] = "sqft"
    row['BHKs'] = data['bhkSplit']

    row['Builder_Logo'] = data['BuilderLogo'] if 'BuilderLogo' in data else None

    row['Unit_Super_Builtup_Area_Min'] = ''
    row['Unit_Super_Builtup_Area_Max'] = ''

    built_area_split = data['BuiltupAreaSqft'].split('to')
    if len(built_area_split) == 2:
        row['Unit_Super_Builtup_Area_Min'] = built_area_split[0]
        row['Unit_Super_Builtup_Area_Max'] = built_area_split[1]
    elif len(built_area_split) == 1:
        row['Unit_Super_Builtup_Area_Min'] = built_area_split[0]

    carpet_area_split = data['bhkSizeRangeSplit'].split(',') if data['bhkSizeRangeSplit'] else []

    units = data['bhkSplit'].split(',')
    row['Unit_Number_Of_Units'] = len(units)

    list_data.append(row)
    for index, u in enumerate(units):
        sub_row = {
            'Project_Name': row['Project_Name'],
            'City': row['City']
        }
        sub_row['Unit_ID'] = index+1
        sub_row['Unit_Name'] = "%s BHK" % u
        sub_row['Unit_Image_Folder'] = "%sBHK_1" % u
        sub_row['Unit_Bedrooms'] = u
        try:
            sub_row['Unit_Carpet_Area_Min'] = carpet_area_split[index].split('-')[0]
        except:
            pass
        try:
            sub_row['Unit_Carpet_Area_Max'] = carpet_area_split[index].split('-')[1]
        except:
            pass
        try:
            sub_row['Unit_Price_Min'] = data['AvgPrice'] * float(only_decimal(sub_row['Unit_Carpet_Area_Min']))
        except:
            pass
        try:
            sub_row['Unit_Price_Max'] = data['AvgPrice'] * float(only_decimal(sub_row['Unit_Carpet_Area_Max']))
        except:
            pass
        sub_row['Operation_Type'] = 'Unit Add'

        list_data.append(sub_row)

    url = 'https://www.sbirealty.in/property/%s/property-for-sale/%s/%s' % (row['City'].lower(), data['ProjectName'].replace(" ", "-", 100), data['ProjectID'].lower())
    browser.get(url)


    try:
        browser.execute_script("window.scrollTo(0, 10000000)")
    except:
        pass

    delay = 15  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sync1 > div.owl-wrapper-outer > div')))
    except TimeoutException:
        pass
    row['Amenities'] = []
    try:
        for i in range(len(browser.find_elements_by_css_selector("#dvAmenities > span"))):
            try:
                row['Amenities'].append(browser.execute_script('return $("#dvAmenities > span:nth-child(%s)").text()' % (i+1)))
            except:
                pass
    except Exception as e:
        row['Amenities'] = []
    row['Amenities'] = ','.join(row['Amenities'])

    try:
        row['RERA'] = browser.find_element_by_css_selector('#sync1 > div.owl-wrapper-outer > span > label').text
    except Exception as e:
        row['RERA'] = ''

    data['Loan_Approvals'] = ''
    try:
        lis = browser.find_element_by_css_selector('#dvProjectDetailContainer').find_elements_by_css_selector('div')
    except:
        lis = []
    for a in lis:
        if 'bank loans' in a.text.lower():
            data['Loan_Approvals'] = a.text.lower().split(':')[1] if a.text.lower().split(':') else ''

    # Images

    row['Image_Folder'] = '%s_%s_%s' % (re.sub('\s', '_', row['Project_Name']), row['City'], today)
    project_root_folder = os.path.join(base_dir, row['Image_Folder'])
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
        pass

    if 'Builder_Logo' in row and row['Builder_Logo']:
        r = requests.get('https://pecon.s3.amazonaws.com/BuilderLogo/%s/%s' % (data['BuilderID'], row['Builder_Logo']))
        with open(os.path.join(project_root_folder, 'project', row['Builder_Logo'].lower()),
                  'wb') as f:
            f.write(r.content)

    # Top images
    top_images = []
    try:
        images = browser.find_element_by_css_selector(
            '#sync1 > div.owl-wrapper-outer > div').find_elements_by_css_selector('div.owl-item')
    except Exception as e:
        images = []

    images = [i.find_element_by_tag_name('img').get_attribute('src') for i in images]

    main_image_found = False
    for x, image in enumerate(images):
        if 'elevation' in image.lower():
            main_image_found = image
            del images[x]
            break
    if not main_image_found and images:
        main_image_found = images[0]
        del images[0]

    if main_image_found:
        if not os.path.exists(os.path.join(project_root_folder, 'project', "Main_1.jpg")):
            r = requests.get(main_image_found)
            with open(os.path.join(project_root_folder, 'project', "Main_1.jpg"), 'wb') as f:
                f.write(r.content)
        sub_row = dict({
            'Project_Name': row['Project_Name'],
            'City': row['City']
        })
        sub_row['Image_Folder'] = main_image_found
        sub_row['Operation_Type'] = 'Image Add'
        list_data.append(sub_row)

    count = 0
    for image in images:
        sub_row = dict({
            'Project_Name': row['Project_Name'],
            'City': row['City']
        })
        sub_row['Image_Folder'] = image
        sub_row['Operation_Type'] = 'Image Add'
        list_data.append(sub_row)

        count += 1
        if not os.path.exists(
                os.path.join(project_root_folder, 'project', 'project_image', str(count) + ".jpg")):
            r = requests.get(image)
            with open(os.path.join(project_root_folder, 'project', 'project_image', str(count) + ".jpg"),
                      'wb') as f:
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
        floors = floor_div.find_elements_by_css_selector('div.tab-pane > div')
    except:
        floors = []

    for a in floors:
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
            if not os.path.exists(
                    os.path.join(project_root_folder, 'unit', name, 'floor_plan', str(index + 1) + ".jpg")):
                r = requests.get(img.get_attribute('href'))
                with open(os.path.join(project_root_folder, 'unit', name, 'floor_plan', str(index + 1) + ".jpg"),
                          'wb') as f:
                    f.write(r.content)

            sub_row = {
                'Project_Name': row['Project_Name'],
                'City': row['City']
            }
            sub_row['Image_Folder'] = img.get_attribute('href')
            sub_row['Operation_Type'] = 'Image Add'
            list_data.append(sub_row)

df = pd.DataFrame(list_data)
df.to_csv('/Users/abhishek/Desktop/olx/sbi-2/sample_sbi_noida.csv', encoding='utf-8')
