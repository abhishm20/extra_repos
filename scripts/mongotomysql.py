from pymongo import MongoClient
from bson import ObjectId


# Mongo Configuration
mongo_db = "db-bd"

def get_mongo_connection():
	return MongoClient("mongodb://localhost:27017")[mongo_db]


def main():
	mongo_connection = get_mongo_connection()
	Outlet = mongo_connection['Outlet']
	outlets = Outlet.find({})
	x = list(outlets)[0]
	for key in x:
		print key, x[key]

if __name__ == '__main__':
	main()