from pymongo import DESCENDING, MongoClient
from mongoconfig import logger
import datetime

#clients = MongoClient("mongodb+srv://csw1594311:csw1594311@cluster0.wp4cz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
clients = MongoClient("mongodb://root:example@localhost:27017/")
logger.info("test")
print(clients.list_database_names())
today = str(datetime.date.today().strftime("%Y%m%d"))
db = clients.mongo_crontab
datas = {
    "compy" : { "code" : "1123", "name" : "ab1c" },
    "date" : "20220518",
    "document" : { "link" : "htt1p:", 
    "title" : "ab1c",
    "script" : "ahamo1"}
}
#db.tdnet.insert_one(datas)
#fromdata = db.tdnet.find({},{"compy":False, "date":False, "document":False})
#fromdata = db.tdnet.find({},{"_id":False,"compy":False, "date":False, "document":False}).sort("id",-1)
fromdata = db.tdnet.find({"date":"20220517", "compy.code":"30540"})
#fromdata = db.tdnet.find().sort({"id",-1})
#fromdata = db.tdnet.find()
        
for i in fromdata :
    # if i["_id"].split("-")[0] == today : 
    #         lastnum = int(i["_id"].split("-")[1])+1
    #         print(lastnum)
    #         break
    print(i)
    # print("code : "+i["compy"]["code"])
    # print("name : "+i["compy"]["name"])
    # print("date : "+i["date"])
    # print("link : "+i["document"]["link"])
    # print("title : "+i["document"]["title"])
    # print("script : "+i["document"]["script"])
    
#print(db.tdnet.find())
#print(db.tdnet.find_one({"author": "developer"}))