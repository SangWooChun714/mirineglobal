from http import client
from pymongo import MongoClient

#clients = MongoClient("mongodb+srv://csw1594311:csw1594311@cluster0.wp4cz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
clients = MongoClient("mongodb://root:example@localhost:8081/")

print(clients.list_database_names())
