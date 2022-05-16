from pymongo import MongoClient

#clients = MongoClient("mongodb+srv://csw1594311:csw1594311@cluster0.wp4cz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
clients = MongoClient("mongodb://root:example@localhost:27017/")

print(clients.list_database_names())

db = clients.mongo_tutorial
datas = {
    'name' : "superman",
    'author' : "DC"
}
inst = db.book.insert_one(datas)
fromdata = db.book.find()
for i in  fromdata:
    print(i)
print(db.book.find())
print(db.book.find_one({"author": "developer"}))