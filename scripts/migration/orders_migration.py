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
def gen_hex_code():
   return ''.join([random.choice('0123456789') for x in range(3)])

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

def get_orderid(outletid):    
    global Conn
    Coll = Conn.Outlet
    try:
        sku = Coll.find_one({'_id': ObjectId(outletid)})
        if sku is not None:
            return sku['outletId']+"--"+str(gen_hex_code()).zfill(3)
        else:
            print "Error", str(gen_hex_code()).zfill(4)+"--"+str(gen_hex_code()).zfill(3)
            return str(gen_hex_code()).zfill(4)+"--"+str(gen_hex_code()).zfill(3)
    except:
        traceback.print_exc()

def get_main_sku(sku_name):
    """
    Get id from name
    """
    global Conn
    Coll = Conn.SKU
    try:
        sku = Coll.find_one({'name': sku_name.lower(), 'grade':'a'})
        if sku is not None:
            return sku
        else:
            [{}]
    except:
        traceback.print_exc()

def get_createdAt(delivery_time):
    return (delivery_time - 86400000 + 43200000 )

def get_dispatchedAt(delivery_time):
    return (delivery_time + 25200000)

def get_deliveredAt(delivery_time):
    return (delivery_time + 36000000)

def get_rating():
    return random.choice(range(3,6))

def create_order_transaction(amount, deliveryDate, transaction_ms, orderId, accountId):
    entry = []
    entry.append(float(amount))
    entry.append('debit')
    entry.append('Purchase - ' + deliveryDate)
    entry.append('')
    entry.append(gen_transation_id())
    entry.append(transaction_ms)
    entry.append(str(orderId))
    entry.append('')
    entry.append(0)
    entry.append(str(accountId))
    entry.append(3)
    try:
        query =  "INSERT INTO transaction  (`amount`,`type`,`title`,`desc`,`transactionId`,`createdAt`, `orderId`, `userId`, `isDeleted`, `accountId`,`temp`)  VALUES %s;" % (tuple(entry),)
        # update_account_query = "update account set `balance`=balance+"-str(amount)+", `updatedAt`="+str(transaction_ms)+" where `id`='"+str(accountId)+"'"
        # cur.execute(update_account_query)
        cur.execute(query)
        db.commit()
        return True
    except:
        traceback.print_exc()
        exit()

def create_order_entry(skus_list, extra_charge_name, extra_charge_amount):
    tempskulist = list(skus_list)
    dd = '2016/06/06'
    oid = 'sdafalwehrwk'
    if(len(tempskulist) > 0):
        dd = tempskulist[0][0]
        oid = tempskulist[0][9]
    order = {}
    orderSku = []
    totalBilledQuantity = 0
    totalDispatchedQuantity = 0
    netAmount = 0
    invoicedAmount = 0
    order['orderId'] = gen_hex_code()
    for (i, each) in enumerate(skus_list):
        main_sku = get_main_sku(each[2].lower())
        order_sku_entry = {}
        order_sku_entry['skuId'] = main_sku['_id']
        order_sku_entry['rate'] = float(each[7])
        order_sku_entry['temp'] = "baba-dhaba"
        order_sku_entry['name'] = main_sku['name']
        order_sku_entry['category'] = main_sku['category']
        order_sku_entry['aliases'] = main_sku['aliases']
        order_sku_entry['hindiName'] = main_sku['hindiName']
        order_sku_entry['quantity'] = float(each[4])
        order_sku_entry['dispatchedQuantity'] = float(each[5])
        order_sku_entry['returnedQuantity'] = float(each[6])
        order_sku_entry['unit'] = each[3].lower()
        order_sku_entry['isDeleted'] = False
        order_sku_entry['createdAt'] = get_createdAt(get_millisecond(each[0]))
        order_sku_entry['updatedAt'] = get_createdAt(get_millisecond(each[0]))

        # orderId for sku

        totalBilledQuantity += order_sku_entry['quantity']
        totalDispatchedQuantity += order_sku_entry['quantity']
        order_sku_entry['amount'] = float(each[8])
        # netAmount += order_sku_entry['amount']
        invoicedAmount += order_sku_entry['amount']
    	print float(each[8]), main_sku['name']
        orderSku.append(order_sku_entry)

    order['deliveryDate'] = get_millisecond(dd)
    d = datetime.datetime.strptime(dd, "%Y/%m/%d")
    order['deliveryDateFormatted'] = d.strftime("%d %b %Y")
    order['status'] = 'delivered'
    order['extraChargeName'] = extra_charge_name
    order['extraChargeAmount'] = extra_charge_amount
    order['outletId'] = ObjectId(oid)
    order['isInvoiced'] = True
    order['temp'] = 10
    order['transporterName'] = each[10]
    order['cratesDispatched'] = 0
    order['cratesReturned'] = 0
    order['balanceCrates'] = 0
    order['isRated'] = True
    order['orderId'] = get_orderid(oid)
    order['rating'] = int(get_rating())
    order['createdAt'] = get_createdAt(get_millisecond(dd))
    order['updatedAt'] = get_deliveredAt(get_millisecond(dd))
    order['isDeleted'] = False
    order['totalBilledQuantity'] = totalBilledQuantity
    order['totalDispatchedQuantity'] = totalDispatchedQuantity
    order['netAmount'] = round(netAmount, 2) + extra_charge_amount 
    order['invoicedAmount'] = round(invoicedAmount, 2) + extra_charge_amount
    order['statusList'] = [{
        "value" : "placed",
        "name" : "Placed",
        "createdAt" : get_createdAt(get_millisecond(dd))
    },
    {
        "value" : "dispatched",
        "name" : "Dispatched",
        "createdAt" : get_dispatchedAt(get_millisecond(dd))
    },
    {
        "value" : "delivered",
        "name" : "Delivered",
        "createdAt" : get_deliveredAt(get_millisecond(dd))
    }]
    global Conn
    global count
    count  += 1
    instance = Conn.Order.insert(order)
    create_order_transaction(order['invoicedAmount'], order['deliveryDateFormatted'], order['updatedAt'], instance, oid)
    for s in orderSku:
        s['orderId'] = ObjectId(instance)
        Conn.OrderSku.insert(s)


count = 0
def upload_orders_csv(file_path):
    data = list(csv.reader(open(file_path, 'rU')))
    data = data[1:]
    data.append([0,0,0,0,0,0,0,0,0])
    prev_outlet = ''
    extra_charge_name = ''
    extra_charge_amount = 0
    prev_date = None
    outlet_orders = []
    for (i, entry) in enumerate(data):
        print entry[0], type(entry[0])
        if(('#N/A' in entry) or ('N/A' in entry) or ('#n/a' in entry)):
            continue
        if(entry[2] == 'Transport' or entry[2] == 'transport' or entry[2] == 'Transportation'):
            extra_charge_name = "Delivery Charge"
            extra_charge_amount = float(entry[8])
            continue
        if((entry[9]!= prev_outlet and prev_outlet != '') or (entry[0]!=prev_date and prev_date != None)):
            create_order_entry(outlet_orders, extra_charge_name, extra_charge_amount)
            extra_charge_name = ''
            extra_charge_amount = 0
            outlet_orders = []
        outlet_orders.append(entry)
        prev_outlet = entry[9]
        prev_date = entry[0]
    print count

if __name__ == '__main__':
    file_path = './o.csv'
    upload_orders_csv(file_path)

