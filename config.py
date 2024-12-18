from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb+srv://zilean12:SJOm5hmafLYXwqjI@cluster0.cszl8.mongodb.net/"
    client = MongoClient(CONNECTION_STRING)
    return client['Dashboard']

db = get_database()
Employees_collection = db['Employee']
Attendance_collection = db['Attendance']
Tasks_collection = db['Task']

