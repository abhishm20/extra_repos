import pymongo
import MySQLdb
from pymongo import MongoClient
import traceback
import datetime
import random
import time
from bson.objectid import ObjectId

# Mongo Config
hostMongo = 'localhost'
portMongo = 27017
dbMongo = 'test'

def createMongoConnection(host, port, db):
    """
    Connector for Mongo database
    """
    client = MongoClient(host, port)
    # coll = cl["local"]["test2"]
    return client[db]

def getAllUsers(Conn):
    Coll = Conn.User
    clients = Coll.find({})
    return list(clients)

def getAllRelation(Conn):
    Coll = Conn.UserOutletRelation
    outlets = Coll.find()
    return list(outlets)

def putOutletTarget(Conn, entry):
    try:
        coll = Conn['Outlet-target']
        key = {'_id':entry['_id']}
        coll.remove(key)
        coll.insert(entry)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    MongoConn = createMongoConnection(hostMongo, portMongo, dbMongo);

    users = getAllRelation(MongoConn)

    count = 0

    for u in users:
        s = {}
        s['userId'] = str(u['userId'])
        s['outletId'] = str(u['outletId'])
        s['_id'] = u['_id']
        s['role'] = u['role']
        putOutletTarget(MongoConn, s)
