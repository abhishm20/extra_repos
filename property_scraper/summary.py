import json
import os
import re

import pandas as pd


def only_number(value):
    regex = re.compile('[^0-9]')
    return regex.sub('', value)


def only_char(value):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', value)


def only_decimal(value):
    regex = re.compile('[^0-9.]')
    return regex.sub('', value)


proptiger = '/Users/abhishek/Desktop/olx/proptiger/links/'
acres = '/Users/abhishek/Desktop/olx/99acres/links/'
sbi = '/Users/abhishek/Desktop/olx/sbi/links/'

data_list = []
for filename in os.listdir(proptiger):
    if not filename.endswith(".json"):
        continue
    filepath = os.path.join(proptiger, filename)
    links = json.loads(open(filepath).read())

    data = {
        'City': filename.split(".")[0],
        'Count': len(links)
    }
    data_list.append(data)

    df = pd.DataFrame(data_list)
    df.to_csv('/Users/abhishek/Desktop/olx/proptiger.csv', encoding='utf-8')

data_list = []
for filename in os.listdir(acres):
    if not filename.endswith(".json"):
        continue
    filepath = os.path.join(acres, filename)
    links = json.loads(open(filepath).read())

    data = {
        'City': filename.split(".")[0],
        'Count': len(links)
    }
    data_list.append(data)

    df = pd.DataFrame(data_list)
    df.to_csv('/Users/abhishek/Desktop/olx/acres.csv', encoding='utf-8')

data_list = []
for filename in os.listdir(sbi):
    if not filename.endswith(".json"):
        continue
    filepath = os.path.join(sbi, filename)
    links = json.loads(open(filepath).read())

    data = {
        'City': filename.split(".")[0],
        'Count': len(links)
    }
    data_list.append(data)

    df = pd.DataFrame(data_list)
    df.to_csv('/Users/abhishek/Desktop/olx/sbi.csv', encoding='utf-8')
