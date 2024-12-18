from flask import jsonify, request
from data_loader import load_data

def Employee_dashboard(Employee_id):
    Employee_data, Attendance_data, Task_data = load_data()
    Employee_info = Employee_data.loc[Employee_data['EmployeeID'] == Employee_id]
    if Employee_info.empty:
        return jsonify({"error": "Employee not found"}), 404
    
    Employee_info = Employee_info.iloc[0]
    Employee_Attendance = Attendance_data[Attendance_data['EmployeeID'] == Employee_id]
    total_hours = int(Employee_Attendance['HoursLogged'].sum())
    Attendance_rate = round((Employee_Attendance['Status'] == 'Present').mean() * 100, 2) if not Employee_Attendance.empty else 0.0

    Employee_Tasks = Task_data[Task_data['EmployeeID'] == Employee_id]['Status'].value_counts().to_dict()

    response = {
        "EmployeeName": Employee_info['Name'],
        "totalHoursLogged": total_hours,
        "AttendanceRate": f"{Attendance_rate}%",
        "Tasks": Employee_Tasks
    }
    return jsonify(response)

def Employee_performance(Employee_id):
    Employee_data, Attendance_data, Task_data = load_data()
    Employee_info = Employee_data.loc[Employee_data['EmployeeID'] == Employee_id]
    if Employee_info.empty:
        return jsonify({"error": "Employee not found"}), 404
    
    Employee_info = Employee_info.iloc[0]
    Employee_Attendance = Attendance_data[Attendance_data['EmployeeID'] == Employee_id]
    total_hours = int(Employee_Attendance['HoursLogged'].sum())
    Attendance_rate = round((Employee_Attendance['Status'] == 'Present').mean() * 100, 2) if not Employee_Attendance.empty else 0.0

    Employee_Tasks = Task_data[Task_data['EmployeeID'] == Employee_id]['Status'].value_counts().to_dict()

    response = {
        "EmployeeName": Employee_info['Name'],
        "totalHoursLogged": total_hours,
        "AttendanceRate": f"{Attendance_rate}%",
        "Tasks": Employee_Tasks
    }
    return jsonify(response)

def Employee_Attendance_trends(Employee_id):
    Employee_data, Attendance_data, Task_data = load_data()
    period = request.args.get('period', 'daily')
    Employee_Attendance = Attendance_data[Attendance_data['EmployeeID'] == Employee_id]

    if period == 'weekly':
        Employee_Attendance['Week'] = Employee_Attendance['Date'].dt.isocalendar().week
        trend_data = Employee_Attendance.groupby('Week')['HoursLogged'].sum()
    elif period == 'monthly':
        Employee_Attendance['Month'] = Employee_Attendance['Date'].dt.month
        trend_data = Employee_Attendance.groupby('Month')['HoursLogged'].sum()
    else:
        trend_data = Employee_Attendance.groupby('Date')['HoursLogged'].sum()

    trend_data = trend_data.reset_index().to_dict(orient='records')
    return jsonify(trend_data)

def Employee_Task_completion(Employee_id):
    Employee_data, Attendance_data, Task_data = load_data()
    Employee_Tasks = Task_data[Task_data['EmployeeID'] == Employee_id]
    period = request.args.get('period', 'weekly')
    if period == 'weekly':
        Employee_Tasks['Week'] = Employee_Tasks['Date'].dt.isocalendar().week
        completed_Tasks = Employee_Tasks[Employee_Tasks['Status'] == 'Completed'].groupby('Week').size()
        total_Tasks = Employee_Tasks.groupby('Week').size()
    elif period == 'monthly':
        Employee_Tasks['Month'] = Employee_Tasks['Date'].dt.month
        completed_Tasks = Employee_Tasks[Employee_Tasks['Status'] == 'Completed'].groupby('Month').size()
        total_Tasks = Employee_Tasks.groupby('Month').size()
    else:
        completed_Tasks = Employee_Tasks[Employee_Tasks['Status'] == 'Completed'].groupby('Date').size()
        total_Tasks = Employee_Tasks.groupby('Date').size()

    completion_rate = (completed_Tasks / total_Tasks * 100).fillna(0).reset_index()
    completion_rate.columns = ['Period', 'CompletionRate']
    return jsonify(completion_rate.to_dict(orient='records'))

