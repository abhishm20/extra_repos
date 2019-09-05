#!/usr/bin/python

# import db_handler
import csv
import datetime
import traceback
from operator import itemgetter
import warnings
import math
import time
import json
import pandas as pd
import numpy as np
import requests
from bson import ObjectId


def get_diff():
    df = pd.read_csv('./ser.csv')
    """
    for finding CLOSED restaurants
    """
    count = 0
    for oo in df['Nov']:
        flag = 0
        for on in df['Jan']:
            if oo==on:
                flag = 1
        if flag == 0:
            count += 1
            print oo
    print count

    """
    for finding NEW restaurants
    """
    # count = 0
    # for oo in df['Jan']:
    #     if str(oo) == 'nan':
    #         continue
    #     flag = 0
    #     for on in df['Nov']:
    #         if oo == on:
    #             flag = 1
    #     if flag == 0:
    #         count += 1
    #         print str(oo)
    # print count

if __name__ == '__main__':
    get_diff()