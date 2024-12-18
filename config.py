from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = ""
    client = MongoClient(CONNECTION_STRING)
    return client['Dashboard']

db = get_database()
Employees_collection = db['Employee']
Attendance_collection = db['Attendance']
Tasks_collection = db['Task']

