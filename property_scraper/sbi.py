# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, json
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# browser = webdriver.Chrome("/Users/abhishek/chromedriver")

delay = 30
df = pd.read_csv('./sbi_locations.csv')

for i, row in df.iterrows():
    filename = '/Users/abhishek/Desktop/sbi/%s.json' % row['name']
    data_list = []
    if not filename.endswith('.json'):
        continue
    with open(filename, 'r+') as f:
        data = json.loads(f.read())
        data = data['d']
        print filename, len(data)
        for i,d in enumerate(data):
            data = {"ProjectId": d['ProjectId']}
            # sending post request and saving response as response object
            url = 'https://www.sbirealty.in/property/SBIAjaxSrv.asmx/GetProjectDetails'
            try:
                r = requests.post(url=url, data=json.dumps(data),
                                  headers={"content-type": "application/json; charset=UTF-8"})
            except Exception as e:
                print d['ProjectId'], 'failed', e
            if r.status_code == 200:
                data_list.append(r.json())
            else:
                print r.status_code
            print i
    with open('/Users/abhishek/Desktop/sbi/data-2/%s.json' % row['name'], 'w') as f:
        json.dump(data_list, f)