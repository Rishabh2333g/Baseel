from flask import send_file
from data_loader import load_data
import matplotlib.pyplot as plt
from io import BytesIO

def visualize_Attendance():
    Employee_data, Attendance_data, Task_data = load_data()
    plt.figure(figsize=(12, 6))
    
    trend_data = Attendance_data.groupby('Date')['HoursLogged'].sum()
    trend_data.plot(kind='line', marker='o')
    plt.title('Daily Hours Logged')
    plt.xlabel('Date')
    plt.ylabel('Hours Logged')
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name="Attendance_trend.png")

def visualize_time_series():
    Employee_data, Attendance_data, Task_data = load_data()
    Attendance_trend = Attendance_data.groupby('Date')['HoursLogged'].sum()
    Task_completion_trend = Task_data.groupby('Date')['Status'].apply(lambda x: (x == 'Completed').sum())

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Hours Logged', color='tab:blue')
    ax1.plot(Attendance_trend.index, Attendance_trend, color='tab:blue', marker='o', label='Attendance')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Completed Tasks', color='tab:green')
    ax2.plot(Task_completion_trend.index, Task_completion_trend, color='tab:green', marker='x', label='Completed Tasks')

    plt.title('Attendance and Task Completion Over Time')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name="time_series.png")


def visualize_Employee_ranking():
    Employee_data, Attendance_data, Task_data = load_data()
    Employee_performance = Attendance_data.groupby('EmployeeID').agg(
        totalHoursLogged=('HoursLogged', 'sum')
    ).reset_index()

    Employee_ranking = Employee_performance.sort_values(by='totalHoursLogged', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(Employee_ranking['EmployeeID'], Employee_ranking['totalHoursLogged'], color='tab:orange')
    plt.title('Top 10 Employees by Hours Logged')
    plt.xlabel('Employee ID')
    plt.ylabel('Hours Logged')
    plt.xticks(Employee_ranking['EmployeeID'], rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name="Employee_ranking.png")

def visualize_summary():
    Employee_data, Attendance_data, Task_data = load_data()
    total_hours = int(Attendance_data['HoursLogged'].sum())
    Attendance_rate = round((Attendance_data['Status'] == 'Present').mean() * 100, 2)
    Tasks_completed = Task_data[Task_data['Status'] == 'Completed'].shape[0]
    
    Task_status_distribution = Task_data['Status'].value_counts()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    ax1.pie(Task_status_distribution, labels=Task_status_distribution.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Task Status Distribution')
    
    metrics = ['Total Hours', 'Attendance Rate', 'Tasks Completed']
    values = [total_hours, Attendance_rate, Tasks_completed]
    ax2.bar(metrics, values)
    ax2.set_title('Summary Metrics')
    ax2.set_ylabel('Value')
    for i, v in enumerate(values):
        ax2.text(i, v, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name="summary_visualization.png")

