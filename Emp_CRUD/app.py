from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
     host='localhost',
     port='5432',
     dbname='employee_data',
     user='postgres',
     password='admin123')

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
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (employee_id,name, email) VALUES (%s, %s, %s)", (employee_id,name, email))
    conn.commit()
    return jsonify({'message': 'Employee created successfully'})

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    conn.commit()
    employee = cur.fetchone()
    if employee is None:
        return jsonify({'message': 'Employee not found'}), 404
    return jsonify(employee)

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    cur = conn.cursor()
    cur.execute("UPDATE employees SET name = %s, email = %s WHERE employee_id = %s", ( name, email, employee_id, ))
    conn.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    conn.commit()
    return jsonify({'message': 'Employee deleted successfully'})

if  __name__=='__main__':
    app.run(debug=True)

