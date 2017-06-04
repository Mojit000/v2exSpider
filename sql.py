from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client.sqw

collectios = db.corp_info