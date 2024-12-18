from flask import Flask, jsonify
from config import get_database, Employees_collection, Attendance_collection, Tasks_collection
from routes.admin_routes import admin_summary, Department_metrics, Employee_ranking, Attendance_trends
from routes.employee_routes import Employee_dashboard, Employee_performance, Employee_Attendance_trends, Employee_Task_completion
from routes.export_routes import export_report
from routes.visualization_routes import visualize_Attendance, visualize_time_series, visualize_Department_comparison, visualize_Employee_ranking, visualize_summary

app = Flask(__name__)

@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        Employees = Employees_collection.find_one()
        Attendance = Attendance_collection.find_one()
        Tasks = Tasks_collection.find_one()
        return jsonify({
            "Employees": Employees,
            "Attendance": Attendance,
            "Tasks": Tasks
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Welcome to Baseel Employee Analytics API! Use the endpoints to fetch data."

# Admin routes
app.route('/admin/summary', methods=['GET'])(admin_summary)
app.route('/admin/Department_metrics', methods=['GET'])(Department_metrics)
app.route('/admin/Employee_ranking', methods=['GET'])(Employee_ranking)
app.route('/admin/Attendance_trends', methods=['GET'])(Attendance_trends)

# Employee routes
app.route('/Employee/<int:Employee_id>', methods=['GET'])(Employee_dashboard)
app.route('/Employee/<int:Employee_id>/performance', methods=['GET'])(Employee_performance)
app.route('/Employee/<int:Employee_id>/Attendance_trends', methods=['GET'])(Employee_Attendance_trends)
app.route('/Employee/<int:Employee_id>/Task_completion', methods=['GET'])(Employee_Task_completion)

# Export route
app.route('/export/<string:report_type>', methods=['GET'])(export_report)

# Visualization routes
app.route('/visualize/Attendance', methods=['GET'])(visualize_Attendance)
app.route('/visualize/time_series', methods=['GET'])(visualize_time_series)
app.route('/visualize/Department_comparison', methods=['GET'])(visualize_Department_comparison)
app.route('/visualize/Employee_ranking', methods=['GET'])(visualize_Employee_ranking)
app.route('/visualize/summary', methods=['GET'])(visualize_summary)

if __name__ == '__main__':
    app.run(debug=False)

