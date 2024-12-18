# Employee Analytics API

## Overview
The **Employee Analytics API** is a Flask-based application designed to provide insights into employee data, attendance, task progress, and performance metrics. It integrates with MongoDB for data storage and uses Pandas for data manipulation and Matplotlib for visualizations.

The API is organized for production use, with modularized code to ensure scalability, maintainability, and reusability.

---

## Features
- **Admin Dashboard**:
  - Summarize employee attendance and task metrics.
  - View department-level performance and top employee rankings.

- **Employee Dashboard**:
  - View individual employee performance metrics.
  - Analyze attendance trends and task completion rates.

- **Visualization**:
  - Generate visual insights such as attendance trends and department comparisons.
  - Export reports and download visualizations.

---

## Project Structure
```
project/
│   ├── routes/
│   │   ├── admin_routes.py   # Admin-related endpoints
│   │   ├── employee_routes.py # Employee-specific endpoints
│   │   ├── visualization_routes.py # Visualization endpoints
│   │   ├── report_routes.py  # Export reports endpoints
├── config.py                 # Configuration settings (MongoDB URI, etc.)
├── data_loader.py            # Load data into Pandas DataFrames
├── app.py                    # main file to run the code
├── requirements.txt          # Python dependencies
```

---

## Prerequisites
- Python 3.8 or higher
- MongoDB instance (local or cloud)
- Pip package manager

---

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rishabh2333g/Baseel.git
   cd Baseel
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**:
   - Update the `MONGO_URI` and `DB_NAME` values in `config.py` to match your MongoDB setup.

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the API**:
   - Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Endpoints
### Admin Dashboard
- **Summary Metrics**: `/admin/summary`
- **Department Metrics**: `/admin/Department_metrics`
- **Employee Rankings**: `/admin/Employee_ranking`
- **Attendance Trends**: `/admin/Attendance_trends?period=[daily|weekly|monthly]`

### Employee Dashboard
- **Employee Details**: `/employee/<employee_id>`
- **Performance Metrics**: `/employee/<employee_id>/performance`

### Visualization
- **Attendance Trends**: `/visualize/Attendance`
- **Employee Rankings**: `/visualize/Employee_ranking`
- **Department Comparison**: `/visualize/Department_comparison`

---

## Testing
1. **Run Unit Tests**:
   Add unit tests under a `tests` directory using the `pytest` framework.
   ```bash
   pytest
   ```

2. **Verify Database Connection**:
   Access the `/test_connection` endpoint to confirm the MongoDB connection is active:
   ```bash
   curl http://127.0.0.1:5000/test_connection
   ```

---

## Future Improvements
- Implement user authentication and authorization.
- Add support for caching frequently accessed data.
- Optimize database queries for large-scale data.
- Create a React-based front-end to visualize insights.
