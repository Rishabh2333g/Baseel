import pandas as pd
from config import Employees_collection, Attendance_collection, Tasks_collection

def load_data():
    global Employee_data, Attendance_data, Task_data
    Employee_data = pd.DataFrame(list(Employees_collection.find()))
    Attendance_data = pd.DataFrame(list(Attendance_collection.find()))
    Task_data = pd.DataFrame(list(Tasks_collection.find()))

    print(f"Loaded {len(Employee_data)} Employee records")
    print(f"Loaded {len(Attendance_data)} Attendance records")
    print(f"Loaded {len(Task_data)} Task records")

    for df in [Employee_data, Attendance_data, Task_data]:
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)

    if 'Date' in Attendance_data.columns:
        Attendance_data['Date'] = pd.to_datetime(Attendance_data['Date'])
    if 'Date' in Task_data.columns:
        Task_data['Date'] = pd.to_datetime(Task_data['Date'])

    return Employee_data, Attendance_data, Task_data

