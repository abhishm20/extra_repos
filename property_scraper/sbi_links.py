# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, json
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome("/Users/abhishek/chromedriver")

delay = 30
df = pd.read_csv('./sbi_locations.csv')

for i, row in df.iterrows():
    browser.get('https://www.sbirealty.in/property/map-view/property-in-%s' % row['key'])
    print row['name']
    try:
        myElem = WebDriverWait(browser, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="dvListContainer"]/div[1]/div/span')))
    except TimeoutException:
        print "Loading took too much time!"

    a = browser.find_element_by_xpath('//*[@id="dvListContainer"]/div[1]/div/span').text
    entries = int(a.split()[0])
    entries = entries if entries < 1000 else 999
    data = {'filter':'{"LocationId":"%s","ColonyId":"","BuilderId":"","ProjectId":"","PriceMin":0,"PriceMax":0,"BHK":"","BHKMin":0,"BHKMax":0,"Segment":"","Amenities":"","Radius":"2","PointOfInterest":"","ProjectSubType":"AC,IF,IV","PageSize":%s,"PageIndex":1,"RecoredPerPage":1,"SizeMin":0,"SizeMax":0,"Latitude":0,"Longitude":0,"IsMapSearch":true,"APF":1,"SortOrder":"Desc","SortBy":"Count","AutoSearchText":"","AutoSearchVal":""}' % (row['key'].split('/')[1].upper(), entries)}
    data = json.loads(json.dumps(data))
    # sending post request and saving response as response object
    url = 'https://www.sbirealty.in/property/SBIAjaxSrv.asmx/GetProjectList'
    r = requests.post(url=url, data=json.dumps(data), headers={"content-type":"application/json; charset=UTF-8"})
    print r.status_code

    with open('/Users/abhishek/Desktop/olx/sbi-2/%s.json' % row['name'], 'w') as f:
        json.dump(r.json(), f)
