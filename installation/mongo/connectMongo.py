import pymongo

userAdmin = "root:"
passAdmin = "rootpassword"
url = "@localhost:27017/"
myclient = pymongo.MongoClient("mongodb://"+userAdmin+passAdmin+url)
mydb = myclient["delivery"]
datas = mydb["applications"]



