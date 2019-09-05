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
mongo_db = 'test'


def create_connection(host, port, db):
    client = MongoClient(host, port)
    return client[db]

Conn = create_connection(host, 27017, mongo_db)

for outlet in list(Conn.Outlet.find()):
	print type(str(outlet['_id']))
	print Conn.UserOutletRelation.find_one({'outletId',str(outlet['_id'])})