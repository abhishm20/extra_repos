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

def create_order_transaction(a):
    entry = []
    entry.append(float(a[2]))
    entry.append('credit')
    entry.append(a[3])
    entry.append(a[4])
    entry.append(gen_transation_id())
    entry.append(float(get_millisecond(a[1])))
    entry.append('')
    entry.append('')
    entry.append(0)
    entry.append(str(a[7]))
    try:
        query =  "INSERT INTO transaction  (`amount`,`type`,`title`,`desc`,`transactionId`,`createdAt`, `orderId`, `userId`, `isDeleted`, `accountId`)  VALUES %s;" % (tuple(entry),)
        # update_account_query = "update account set `balance`=balance+"-str(amount)+", `updatedAt`="+str(transaction_ms)+" where `id`='"+str(accountId)+"'"
        # cur.execute(update_account_query)
        cur.execute(query)
        db.commit()
        return True
    except:
        traceback.print_exc()
        exit()

def upload_orders_csv(file_path):
    data = list(csv.reader(open(file_path, 'rU')))
    data = data[1:]
    count = 0
    for (i, entry) in enumerate(data):
      count += 1
      print count, entry[1]
      create_order_transaction(entry)
    print count

if __name__ == '__main__':
    file_path = './DebtorsSummary.csv'
    upload_orders_csv(file_path)

