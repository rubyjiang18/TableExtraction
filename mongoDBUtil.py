from pymongo import MongoClient

cluster = "mongodb://table_extraction:vlldc3JRnDG2DvW3@cluster0-shard-00-00.afvrd.mongodb.net:27017,cluster0-shard-00-01.afvrd.mongodb.net:27017,cluster0-shard-00-02.afvrd.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-12bs5c-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(cluster)

db = client.data

db.Refractory_Alloys.update_many({}, {"$set": {"Flag": False}})