from flask import jsonify, request
from data_loader import load_data

def admin_summary():
    Employee_data, Attendance_data, Task_data = load_data()
    total_hours = int(Attendance_data['HoursLogged'].sum())
    average_hours = float(Attendance_data['HoursLogged'].mean()) if not Attendance_data['HoursLogged'].empty else 0.0
    Attendance_rate = round((Attendance_data['Status'] == 'Present').mean() * 100, 2)

    Tasks_completed = int(Task_data[Task_data['Status'] == 'Completed'].shape[0])
    Tasks_in_progress = int(Task_data[Task_data['Status'] == 'In Progress'].shape[0])
    Tasks_not_started = int(Task_data[Task_data['Status'] == 'Not Started'].shape[0])

    response = {
        "totalHoursLogged": total_hours,
        "averageHoursLogged": round(average_hours, 2),
        "AttendanceRate": f"{Attendance_rate}%",
        "TasksCompleted": Tasks_completed,
        "TasksInProgress": Tasks_in_progress,
        "TasksNotStarted": Tasks_not_started
    }
    return jsonify(response)

def Department_metrics():
    Employee_data, Attendance_data, Task_data = load_data()
    Department_metrics = Employee_data.merge(Attendance_data, on="EmployeeID").merge(Task_data, on="EmployeeID")
    Department_summary = Department_metrics.groupby('Department').agg(
        totalHoursLogged=('HoursLogged', 'sum'),
        TasksCompleted=('TaskID', lambda x: (x.notnull()).sum())
    ).reset_index()

    response = Department_summary.to_dict(orient='records')
    return jsonify(response)

def Employee_ranking():
    Employee_data, Attendance_data, Task_data = load_data()
    Employee_performance = Attendance_data.groupby('EmployeeID').agg(
        totalHoursLogged=('HoursLogged', 'sum')
    ).reset_index()

    Employee_performance = Employee_performance.merge(
        Task_data.groupby('EmployeeID').agg(
            TasksCompleted=('TaskID', lambda x: (x.notnull()).sum())
        ).reset_index(),
        on='EmployeeID'
    )

    Employee_ranking = Employee_performance.sort_values(by='totalHoursLogged', ascending=False)
    Employee_ranking = Employee_ranking.head(10)

    response = Employee_ranking.to_dict(orient='records')
    return jsonify(response)

def Attendance_trends():
    Employee_data, Attendance_data, Task_data = load_data()
    period = request.args.get('period', 'daily')

    if period == 'weekly':
        Attendance_data['Week'] = Attendance_data['Date'].dt.isocalendar().week
        trend_data = Attendance_data.groupby('Week')['HoursLogged'].sum()
    elif period == 'monthly':
        Attendance_data['Month'] = Attendance_data['Date'].dt.month
        trend_data = Attendance_data.groupby('Month')['HoursLogged'].sum()
    else:
        trend_data = Attendance_data.groupby('Date')['HoursLogged'].sum()

    trend_data = trend_data.reset_index().to_dict(orient='records')
    return jsonify(trend_data)

