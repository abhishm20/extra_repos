import pymongo
import MySQLdb
from pymongo import MongoClient
import traceback
import datetime
import random
import time

# Mongo Config
hostMongo = 'localhost'
portMongo = 27017
dbMongo = 'test2'

# Mysql Config
hostMySQL = 'localhost'
portMySQL = '3306'
userMySQL = 'root'
passwdMySQL = 'ainaa'

# Util Function
def gen_hex_colour_code():
   return ''.join([random.choice('0123456789ABCDEF') for x in range(4)])

def createMongoConnection(host, port, db):
    """
    Connector for Mongo database
    """
    client = MongoClient(host, port)
    # coll = cl["local"]["test2"]
    return client[db]

def createMysqlConnection(host, port, user, passwd):
    """
    Connector for Mysql database
    """
    db = MySQLdb.connect(host=host,user=user,passwd=passwd)
    return db

def closeMysqlConnection(connection):
    """
    Connector for Mysql database
    """
    return connection.close()

def executeMysqlQuery(conn, query):
    """
    Create Table for Mysql Table
    """
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()

def getAllClients(Conn):
    Coll = Conn.Client
    clients = Coll.find({})
    return list(clients)

def getAllOutlets(Conn, client_id):
    Coll = Conn.Outlet
    outlets = Coll.find({'clientId': client_id})
    return list(outlets)

def getAllManagers(Conn):
    Coll = Conn.Manager
    managers = Coll.find({})
    return list(managers)

def getAllPurchasers(Conn):
    Coll = Conn.Purchaser
    purchasers = Coll.find({})
    return list(purchasers)

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
    MysqlConn = createMysqlConnection(hostMySQL, portMySQL, userMySQL, passwdMySQL);

    OutletAccountTableCreateQuery = "\
        CREATE TABLE Account (\
        id varchar(255) NOT NULL,\
        balance double(20,2) NOT NULL,\
        updatedAt bigint(20) DEFAULT NULL,\
        createdAt bigint(20) NOT NULL,\
        isDeleted tinyint(1) DEFAULT NULL,\
        PRIMARY KEY (id)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    SalesPersonAccountTableCreateQuery = """
        CREATE TABLE SPAccount (
        id varchar(255) NOT NULL,
        balance double(20,2) NOT NULL,
        updatedAt bigint(20) DEFAULT NULL,
        createdAt bigint(20) NOT NULL,
        isDeleted tinyint(1) DEFAULT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """

    SalesPersonTransactionTableCreateQuery = """
        CREATE TABLE `SPTransaction` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `amount` double(20,2) NOT NULL,
      `type` varchar(512) NOT NULL,
      `title` varchar(1000) NOT NULL,
      `desc` text,
      `transactionId` varchar(512) NOT NULL,
      `createdAt` bigint(20) DEFAULT NULL,
      `isDeleted` tinyint(1) DEFAULT NULL,
      `spAccountId` varchar(512) DEFAULT NULL,
      `outletId` varchar(512) DEFAULT NULL,
      `isCommission` tinyint(1) DEFAULT '1',
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
    """

    OutletTransactionTableCreateQuery = """
        CREATE TABLE `Transaction` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `amount` double(20,2) NOT NULL,
          `type` varchar(512) NOT NULL,
          `title` varchar(1000) NOT NULL,
          `desc` text,
          `transactionId` varchar(512) NOT NULL,
          `createdAt` bigint(20) DEFAULT NULL,
          `orderId` varchar(512) DEFAULT NULL,
          `userId` varchar(512) DEFAULT NULL,
          `isDeleted` tinyint(1) DEFAULT NULL,
          `accountId` varchar(512) DEFAULT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
    """

    # executeMysqlQuery(MysqlConn, "CREATE DATABASE db_bd");
    # executeMysqlQuery(MysqlConn, "use migration");
    # executeMysqlQuery(MysqlConn, OutletAccountTableCreateQuery)
    # executeMysqlQuery(MysqlConn, SalesPersonAccountTableCreateQuery)
    # executeMysqlQuery(MysqlConn, SalesPersonTransactionTableCreateQuery)
    # executeMysqlQuery(MysqlConn, OutletTransactionTableCreateQuery)

    clients = getAllClients(MongoConn)

    count = 0
    for (i, client) in enumerate(clients):
        client_id = client.get('_id', '')
        outlets = getAllOutlets(MongoConn, client_id)
        for (j, outlet) in enumerate(outlets):
            count += 1
            try:
                data = {}
                data['_id'] = outlet['_id']
                data['name'] = client['name'] + ' ' + outlet['name']
                print count, data['name'], data['_id']
                data['lowerName'] = data['name'].lower()
                data['creditLimit'] = client['_account']['limit']
                data['paymentMode'] = client['paymentMode']
                data['billingName'] = client['billingName']
                data['paymentCycle'] = client['paymentCycle']
                data['createdAt'] = outlet['createdAt']
                data['updatedAt'] = outlet['updatedAt']
                data['isActive'] = outlet['isActive']
                data['isDeleted'] = outlet['isDeleted']
                data['email'] = client['emails'][0] if client['emails'] else ""
                data['rateSlab'] = outlet['rateSlab']
                data['_address'] = outlet['_address']
                data['pendingCrates'] = outlet['pendingCrates']
                data['returningWindow'] = outlet['returningWindow']
                data['freezeTime'] = int(outlet['freezeTime'].split(":")[0])*3600*1000+ int(outlet['freezeTime'].split(":")[1])*60*1000
                data['outletId'] = gen_hex_colour_code()
                data['isDeleted'] = outlet['isDeleted']
                data['landline'] = outlet['_address']['landline']

                acc = client['_account']
                OutletAccountTableInsertQuery = "INSERT INTO `Account` (`id`, `balance`,`updatedAt`,`createdAt`,`isDeleted`) VALUES ('%s', %d, %d, %d, %d);" % (data['_id'], acc['balance'], acc['updatedAt'] or 0, outlet['createdAt'] or 0, data['isDeleted'])
                # print OutletAccountTableInsertQuery
                # executeMysqlQuery(MysqlConn, OutletAccountTableInsertQuery)
                putOutletTarget(MongoConn, data)
            except:
                traceback.print_exc()
    MysqlConn.commit()

    managers = getAllManagers(MongoConn)
    purchasers = getAllPurchasers(MongoConn)

    count = 0
    for (i, each) in enumerate(managers + purchasers):
        try:
            data = {}
            if(each in managers):
                data['role'] = 'manager'
            if(each in purchasers):
                data['role'] = 'purchaser'
            if(data['role'] is 'manager'):
                outlets = MongoConn.Outlet.find({'clientId': each['clientId']}).distinct('_id')
                data['outletIds'] = outlets
            if(data['role'] is 'purchaser'):
                data['outletIds'] = each['outletIds']

            data['_id'] = each['_id']
            data['name'] = each['name']
            data['mobile'] = each['mobile']
            data['email'] = each['email']
            data['originalPassword'] = ''
            data['password'] = each['password']
            data['isActive'] = each['isActive']
            data['isDeleted'] = each['isDeleted']
            data['createdAt'] = each['createdAt']
            data['updatedAt'] =  each.get('updatedAt', each['createdAt'])
            data['isVerified'] = True
            count += 1
            print count, data['name'], data['mobile'], data['_id']
            MongoConn['User-target'].update({'_id':each['_id'], 'mobile':each['mobile']}, data, upsert=True)

            for outletId in data['outletIds']:
                relationData = {}
                relationData['userId'] = data['_id']
                relationData['outletId'] = outletId
                relationData['role'] = data['role']
                MongoConn['UserOutletRelation'].insert(relationData)
        except:
            traceback.print_exc()
