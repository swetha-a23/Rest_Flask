from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='new_employee',
    user='postgres',
    password='admin123'
)

cur = conn.cursor()

conn.commit()

@app.route('/employees', methods=['GET'])
def get_employees():
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    return jsonify(employees)

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee_id = data['employee_id']
    name = data['name']
    email = data['email']
    department_id = data['department_id']
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (employee_id, name, email, department_id) VALUES (%s, %s, %s, %s)", (employee_id, name, email, department_id))
    conn.commit()
    return jsonify({'message': 'Employee created successfully'})

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    employee = cur.fetchone()
    if employee is None:
        return jsonify({'message': 'Employee not found'}), 404
    return jsonify(employee)

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    department_id = data['department_id']
    cur = conn.cursor()
    cur.execute("UPDATE employees SET name = %s, email = %s, department_id = %s WHERE employee_id = %s",
                (name, email, department_id, employee_id))
    conn.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    conn.commit()
    return jsonify({'message': 'Employee deleted successfully'})

@app.route('/departments', methods=['GET'])
def get_departments():
    cur = conn.cursor()
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()
    return jsonify(departments)

@app.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json()
    department_id=data['department_id']
    name = data['name']
    cur = conn.cursor()
    cur.execute("INSERT INTO departments (department_id,name) VALUES (%s, %s)", (department_id, name,))
    conn.commit()
    return jsonify({'message': 'Department created successfully'})

@app.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM departments WHERE department_id = %s", (department_id,))
    department = cur.fetchone()
    if department is None:
        return jsonify({'message': 'Department not found'}), 404
    return jsonify(department)

@app.route('/departments/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    data = request.get_json()
    name = data['name']
    cur = conn.cursor()
    cur.execute("UPDATE departments SET name = %s WHERE department_id = %s", (name, department_id))
    conn.commit()
    return jsonify({'message': 'Department updated successfully'})

@app.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM departments WHERE department_id = %s", (department_id,))
    conn.commit()
    return jsonify({'message': 'Department deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
