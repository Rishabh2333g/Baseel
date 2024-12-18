from flask import jsonify, request, send_file
from data_loader import load_data
from io import BytesIO

def export_report(report_type):
    Employee_data, Attendance_data, Task_data = load_data()
    buffer = BytesIO()

    if report_type == 'admin':
        report_data = Attendance_data.merge(Employee_data, on="EmployeeID").merge(Task_data, on="EmployeeID")
    else:
        Employee_id = request.args.get('Employee_id')
        if not Employee_id or not Employee_id.isdigit():
            return jsonify({"error": "Valid Employee_id is required"}), 400
        Employee_id = int(Employee_id)
        report_data = Attendance_data[Attendance_data['EmployeeID'] == Employee_id]
        if report_data.empty:
            return jsonify({"error": "No data found for this Employee"}), 404

    report_data.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{report_type}_report.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

