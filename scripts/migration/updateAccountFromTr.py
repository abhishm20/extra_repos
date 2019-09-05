import pymongo
from pymongo import MongoClient
import traceback
import datetime
import random
import time
from bson import ObjectId
import csv
import MySQLdb

db = MySQLdb.connect(host="localhost",user="root",passwd="ainaa", db="db_bd")
cur = db.cursor()

def gen_transation_id():
   return ''.join([random.choice('0123456789ABCDEF') for x in range(13)])

def get_millisecond(date_str):
    """
    Get timestamp in milliseconds from date string of format m/d/yyyy
    """
    d = datetime.datetime.strptime(date_str, "%Y/%m/%d")
    return time.mktime(d.timetuple()) * 1000

def getFinalAmount(id):
    try:
        query =  "Select * from Transaction where accountId='"+str(id)+"'";
        cur.execute(query)
        trs = list(cur)
        finalAmount = 0
        for t in trs:
            if(t[2] == 'credit'):
                finalAmount += t[1]
            else:
                finalAmount -= t[1]
        print finalAmount
        update_account_query = "update account set `balance`= "+str(finalAmount)+" where `id`='"+str(id)+"'";
        print update_account_query
        cur.execute(update_account_query)
        db.commit()
        return True
    except:
        traceback.print_exc()
        exit()

def getAccounts():
    try:
        query =  'Select * from Account';
        cur.execute(query)
        accounts = list(cur)
        for a in accounts:
            getFinalAmount(a[0])
        db.commit()
        return True
    except:
        traceback.print_exc()
        exit()


if __name__ == '__main__':
    getAccounts()