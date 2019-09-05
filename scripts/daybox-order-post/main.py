#!/usr/bin/python

# import db_handler
import csv
import datetime
import json

import requests

headers = {'content-type': 'application/json', 'Authorization': "Basic 512c6081e28acca197ba6de0c590875f"}
base_url = 'https://bdapi.daybox.in/api/v1/Outlets/ID/orders'


poso_order_url = "http://testapi.daybox.in:3000/v1/api/Orders/supplierWise?date=DELIVERY_DATE"
poso_headers = {'Authorization':json.dumps({"secret":"3fe76ec0-cb9b-11e6-9932-592a417f7eaf","id":"58450c1179d7606e4c706cd5","role":"admin","realm":"web"}), 'content-type': 'application/json'}


count = 0


def create_order_entry(outletId, outlet_orders, deliveryDate, amount, extra_charge_name, extra_charge_amount):
    global base_url
    if amount < 1000:
        extra_charge_name = 'Transport'
        extra_charge_amount = 300
        amount += 300
    order = {
        "userId": "",
        "dontCheckForDuplicateOrder": False,
        "netAmount": amount,
        "invoicedAmount": amount,
        "extraChargeName": extra_charge_name,
        "extraChargeAmount": extra_charge_amount,
        "deliveryDate": str(int(deliveryDate)+19800000),
        "skus":outlet_orders
    }
    # print order
    url = base_url.replace("ID",outletId)
    r = requests.post(url, data=json.dumps(order), headers=headers)
    print r.reason, r.json()
    print r.status_code, amount
    return 0


def get_outlet_id(id):
    if id == '584e9cf5402784ae629419b5': # bercos sohna road
        return '578662ae2f39318a20f16226'
    elif id == '5842b2d0a1c591680323e596': # Biryani paradise sohna road
        return '57e554938f19644f716ed372'
    elif id == '584e4bc80a9dc5963b52af9a': # Bercos GK1
        return '579c92b8a46e065371f88e1a'
    elif id == '584be585f0c8599911682885': # To be healthy
        return '57ac50ac0a3eff561ead0072'
    else:
        print "outlet not found "+id
        exit()


def get_found_item(df, order, item):
    for (i, entry) in enumerate(df):
        if entry[1] == item['itemId'] and entry[0] == order['outlet']['id']:
            return entry

def get_poso_orders():
    df = list(csv.reader(open('./mapping.csv', 'rU')))
    df = df[1:]
    # df = "pd.read_csv('./mapping.csv')
    # delivery_date = "(datetime.date.today()).strftime("%s")+ "000"
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%s") + "000"
    url = poso_order_url.replace("DELIVERY_DATE", delivery_date)
    print url
    r = requests.get(url, headers=headers)
    orders = json.loads(r.content)['response']
    for o in orders:
        if o['supplier']['id'] == '5842b460a1c591680323e671':
            for order in o['orders']:
                # if order['isOrderApproved'] is False:
                    # continue
                items = []
                total_amount = 0
                for item in order['items']:
                    print item['name'], order['outlet']['name']
                    found_item = get_found_item(df, order, item)
                    # found_item = "df[(df['poso_id'] == "item['itemId']) & ( df['outlet_id'] == "order['outlet']['id'])].reset_index()
                    i = {
                        "name": found_item[3],
                        "rate": item['rate'],
                        "amount": item['amount'],
                        "unit": str(found_item[5]),
                        "id": (found_item[2]),
                        "hindiName": (found_item[4]),
                        "quantity": float(item['quantityOrdered'])
                    }
                    total_amount += (i['rate'] * i['quantity'])
                    items.append(i)
                # print get_outlet_id(order['outlet']['id']), items, delivery_date, total_amount
                create_order_entry(get_outlet_id(order['outlet']['id']), items, delivery_date, total_amount,"",0)

if __name__ == '__main__':
    get_poso_orders()