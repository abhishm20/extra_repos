from pymongo import MongoClient
import MySQLdb
import config


def get_mongo_connection():
    return MongoClient('mongodb://localhost:27017')[config.MONGO_DB]


def get_mysql_connection():
    db = MySQLdb.connect(host="localhost", user="root", passwd="ainaa", db="db_bd")
    return db.cursor()


def create_metadata_relation_table(connection):
    connection.execute(config.METADATA_RELATION_TABLE)


def main():
    mysql_connection = get_mysql_connection()
    create_metadata_relation_table(mysql_connection)
    mongo_connection = get_mongo_connection()
    collection_list = mongo_connection.collection_names()
    print "Select one table?"
    for i in range(len(collection_list)):
        print "{}. {}".format(i, collection_list[i])
    input = int(raw_input("? "))
    if(input >= 0 and input <= len(collection_list)):
        print "You selected "+collection_list[input]
    else:
        raw_input("Enter the correct no. ");


if __name__ == '__main__':
    main()