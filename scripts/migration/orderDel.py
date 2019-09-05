import pymongo
from bson import ObjectId
from pymongo import MongoClient
import MySQLdb
import traceback

import re
regx = re.compile("--", re.IGNORECASE)
regxDeliveryDate = re.compile("Aug 2016")

host = 'localhost'
port = 27017
db = 'test'


mysql_db = MySQLdb.connect(host="localhost",user="root",passwd="ainaa", db="db_bd")
cur = mysql_db.cursor();

client = MongoClient(host, port)
Coll_order = client[db]['Order']
Coll_orderSku = client[db]['OrderSku']

orders = Coll_order.find({"orderId":regx, "outletId":ObjectId("57c42da9218be744e698e8a4"), "deliveryDateFormatted": regxDeliveryDate})

count = 0
for order in orders:
    orderId = order.get('_id', None)
    print orderId
    count += 1
    if(orderId):
        Coll_orderSku.remove({'orderId': ObjectId(orderId)})
        Coll_order.remove({'_id': ObjectId(orderId)})
        try:
        	query =  "DELETE FROM `db_bd`.`Transaction` WHERE `orderId`='"+str(orderId)+"';"
        	print query
        	cur.execute(query)
       		mysql_db.commit()
    	except:
        	traceback.print_exc()
        	exit()

print count