# import os
import datetime
from pymongo import MongoClient

# ! For Heroku
# * cluster = MongoClient(os.environ['MONGODB_URI'])

cluster = MongoClient("mongodb+srv://admin:admin@clustercaviar.q2vr5.mongodb.net/caviardb?retryWrites=true&w=majority")
db = cluster["caviardb"]

clients_collect = db["clients"]
orders_collect = db["orders"]


def maxIndex():
    max_id = None
    idx = clients_collect.find({}).sort("_id", -1).limit(1)
    if idx is not None:
        for data in idx:
            max_id = data["_id"]
    else:
        max_id = 1
    return max_id

def getClientInfo(id):
    user = clients_collect.find_one(
        {
            "client_id" : id
        }
    )

    user2 = clients_collect.find_one(
        {
            "client_id" : id
        }
    )["username"]

    print(user)
    print(user2)

def addClient(id, user, first_name, last_name):
    count_now = maxIndex()

    data = {
        "_id" : 2,
        "client_id" : id,
        "username" : user,
        "first_name" : first_name,
        "last_name" : last_name,
        "phone" : "",
        "location" : "",
        "created" : datetime.datetime.now()
    }

    clients_collect.insert_one(data)
    ids = data["_id"]

    print(f"Add success: {ids}")

def addClientInfo():
    pass


def clearDB():
    clients_collect.delete_many({ "client_id" : 123546789 })
    print("Delet Done")
    for i in clients_collect.find():
        print(i)
    

if __name__ == "__main__":
    # addClient(123546789, "alukarZ", "MaksimdddZ", "michurindddZ")
    # getClientInfo(123546789)
    print(f"Max index find: {maxIndex()}")
    # maxIndex()
    # clearDB()
    # print(f"Max index find after del: {maxIndex()}")
