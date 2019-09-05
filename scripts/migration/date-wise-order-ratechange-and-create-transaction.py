import pymongo
from pymongo import MongoClient
import traceback
import datetime
import random
import time
from bson import ObjectId
import csv
import MySQLdb

host = 'localhost'
port = 27017
mongo_db = 'local'

db = MySQLdb.connect(host="localhost",user="root",passwd="ainaa", db="db_bd")
cur = db.cursor();

def gen_transation_id():
   return ''.join([random.choice('0123456789ABCDEF') for x in range(13)])

def get_millisecond(date_str):
    """
    Get timestamp in milliseconds from date string of format m/d/yyyy
    """
    d = datetime.datetime.strptime(date_str, "%Y/%m/%d")
    return time.mktime(d.timetuple()) * 1000

def create_connection(host, port, db):
    """
    Connector for database
    """
    client = MongoClient(host, port)
    # coll = cl["local"]["test2"]
    return client[db]

Conn = create_connection(host, 27017, mongo_db)

def get_order(outletId ,dd):
    global Conn
    Coll = Conn.Order
    try:
        sku = Coll.find_one({'outletId': ObjectId(outletId), 'deliveryDateFormatted':dd})
        return sku
    except:
        traceback.print_exc()

def get_order_skus(orderId):
    global Conn
    Coll = Conn.OrderSku
    try:
        skus = Coll.find({'orderId': orderId})
        if skus is not None:
            return skus
        else:
            print "sku not found"
    except:
        traceback.print_exc()

def get_sku_from_list(skuList, name):
    for x in skuList:
        if(x[2] == name):
            return x
    print "asdfjlkasdjlfjalksdjlfjalsjdlfakjsldflaksdjfl"

def get_order_extra_charge(skuList):
    for x in skuList:
        if(x[2] == "Transportation"):
            return x[7]
    return 0
    print "asdfjlkasdjlfjalksdjlfjalsjdlfakjsldflaksdjfl"

def create_order_transaction(amount, deliveryDate, transaction_ms, orderId, accountId):
    entry = []
    entry.append(float(amount))
    entry.append('debit')
    entry.append(str('Purchase - ' + deliveryDate))
    entry.append('')
    entry.append(gen_transation_id())
    entry.append(transaction_ms)
    entry.append(str(orderId))
    entry.append('')
    entry.append(0)
    entry.append(str(accountId))
    try:
        query =  "INSERT INTO transaction  (`amount`,`type`,`title`,`desc`,`transactionId`,`createdAt`, `orderId`, `userId`, `isDeleted`, `accountId`)  VALUES %s;" % (tuple(entry),)
        # update_account_query = "update account set `balance`=balance+"-str(amount)+", `updatedAt`="+str(transaction_ms)+" where `id`='"+str(accountId)+"'"
        # cur.execute(update_account_query)
        # print query
        cur.execute(query)
        db.commit()
        return True
    except:
        traceback.print_exc()
        exit()
count = 0
def create_order_entry(skus_list, extra_charge_name, extra_charge_amount):
    global Conn
    global count
    OrderSkuColl = Conn.OrderSku
    OrderColl = Conn.Order
    
    tempskulist = list(skus_list)
    deliveryDate = "12 Sep 2016"
    dd = ''
    oid = ''
    if(len(tempskulist) <= 0):
        return

    order = {}
    orderSku = []
    netAmount = 0
    invoicedAmount = 0
    print skus_list[0][8]
    orderInstance = get_order(skus_list[0][8], deliveryDate)
    orderSkus = get_order_skus(orderInstance['_id'])
    for (i, each) in enumerate(list(orderSkus)):
        count += 1
        OrderSkuColl.update({
            '_id': each['_id']
            },{
            '$set': {
                'rate':float(get_sku_from_list(skus_list, each['name'])[6]),
                'amount':float(get_sku_from_list(skus_list, each['name'])[7]),
                'x':2
            }
        }, upsert=False, multi=False)
        
        netAmount += float(get_sku_from_list(skus_list, each['name'])[7])
        invoicedAmount += float(get_sku_from_list(skus_list, each['name'])[7])

    extra_amount = get_order_extra_charge(skus_list)
    if(extra_amount != 0):
        count += 1
        OrderColl.update({
                '_id': orderInstance['_id']
                },{
                '$set': {
                    'extraChargeName':"Delivery",
                    'extraChargeAmount':float(extra_amount),
                    'x':2
                }
            }, upsert=False, multi=False)
        netAmount += float(extra_amount)
        invoicedAmount += float(extra_amount)
    instance = OrderColl.update({
            '_id': orderInstance['_id']
            },{
            '$set': {
                'netAmount':netAmount,
                'invoicedAmount':invoicedAmount,
                'x':2
            }
        }, upsert=False, multi=False)
    create_order_transaction(invoicedAmount, orderInstance['deliveryDateFormatted'], orderInstance['updatedAt'], str(orderInstance['_id']), skus_list[0][8])


def upload_orders_csv(file_path):
    global count
    data = list(csv.reader(open(file_path, 'rU')))
    data = data[1:]
    data.append([0,0,0,0,0,0,0,0,0])
    prev_outlet = ''
    extra_charge_name = ''
    extra_charge_amount = 0
    prev_date = None
    outlet_orders = []
    for (i, entry) in enumerate(data):
        # print entry[0], type(entry[0])
        if(('#N/A' in entry) or ('N/A' in entry) or ('#n/a' in entry)):
            continue
        if(entry[2] == 'Transport' or entry[2] == 'transport'):
            extra_charge_name = "Delivery Charge"
            extra_charge_amount = float(entry[7])
            continue
        if((entry[8]!= prev_outlet and prev_outlet != '') or (entry[0]!=prev_date and prev_date != None)):
            create_order_entry(outlet_orders, extra_charge_name, extra_charge_amount)
            extra_charge_name = ''
            extra_charge_amount = 0
            outlet_orders = []
        outlet_orders.append(entry)
        prev_outlet = entry[8]
        prev_date = entry[0]
    print count

if __name__ == '__main__':
    file_path = './Ordersdata.csv'
    upload_orders_csv(file_path)

