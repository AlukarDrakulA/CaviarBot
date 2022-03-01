# import os
import datetime
from pymongo import MongoClient

# ! For Heroku
# * cluster = MongoClient(os.environ['MONGODB_URI'])

cluster = MongoClient("mongodb+srv://admin:admin@clustercaviar.q2vr5.mongodb.net/caviardb?retryWrites=true&w=majority")
db = cluster["caviardb"]

clients_collect = db["clients"]
orders_collect = db["orders"]


def getClientInfo(clientId):
    user = clients_collect.find_one({"client_id" : clientId})

    data_result = []

    data_result.append(user["username"])
    data_result.append(user["first_name"])
    data_result.append(user["last_name"])
    data_result.append(user["location"])
    data_result.append(user["phone"])

    return data_result


def addClient(id, user, first_name, last_name):
    data = {
        "client_id" : id,
        "username" : user,
        "first_name" : first_name,
        "last_name" : last_name,
        "phone" : None,
        "location" : None,
        "created" : datetime.datetime.now()
    }

    user_add = data["username"]
    id_add = data["client_id"]

    if clients_collect.count_documents({ "client_id" : id }) == 0:
        clients_collect.insert_one(data)
        print(f"[INFO] - New user added: Username: {user_add} | ID: {id_add}")
    else:
        print(f"[INFO] - The user {id_add} is already in the database. Continue...")


def addClientInfo(data, id, status):
    if status == 'phone':
        clients_collect.update_one({"client_id" : id}, {"$set": {"phone" : int(data)}})
        print(f"Add phone {data} to client {id}")
    elif status == 'location':
        clients_collect.update_one({"client_id" : id}, {"$set": {"location" : data}})
        print(f"Add locaton {data} to client {id}")
    else:
        pass

def addOrder(user):
    cl = None
    g = clients_collect.find({"username" : "alukarZ"})

    for i in g:
        cl = i["_id"]

    print(cl)

    data = ({
        "client_id" : {"$ref" : "clients", "$id" : cl},
        "type" : "kizhuch_3",
        "username" : user
    })

    orders_collect.insert_one(data)
    print(f"Add new order: {data}")
   

def createOrder():
    pass

if __name__ == "__main__":
    pass
    # addClient(123456789, "alukarZ", "MaksimdddZ", "michurindddZ")
    # # addOrder("alukarZ")
    # a = getClientInfo(123456789)
    # if a[3] is NULL:
    #     print("eto pusto")
    # else:
    #     print(f"ne pusto")
    # print(a[3])
    # print(f"Max index find: {maxIndex()}")
    # maxIndex()
    # clearDB()
    # print(f"Max index find after del: {maxIndex()}")

    # u = clients_collect.find_one({"username" : "alukarZ"})
    # print(f"U: {u}")
    # d = orders_collect.find({"client_id" : u["client_id"]})
    # for i in d:
    #     print(f"D: {i}")

    # # ? DBRef
    # o = orders_collect.find_one({"type" : "kizhuch_3"})
    # dbref = o["client_id"].as_doc()
    # oid = dbref.get("$id")

    # print(clients_collect.find_one({"_id" : oid}))

    # print(f"O: {o}")
    # d = clients_collect.find_one({"client_id" : o["client_id"]})
    # print(f"d: {d}")
