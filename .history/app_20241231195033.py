from flask import Flask
from flask import request
from flask import jsonify
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json


app = Flask(__name__)

host = 'localhost'
user = 'root'   # replace with your MySQL username
password = 'dougfunny'  # replace with your MySQL password
database = 'fitness_center'  # replace with your database name


def get_db_connection():
    connection = mysql.connector.connect(
        host=host,
        user= user,
        password=password,
        database=database
    )
    if connection.is_connected():
        return connection
    else:
        raise Exception("Failed to connect to the database")

#Task 1: CRUD Operations for Members
#create a new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    
    if not name or not email or not phone:
        (400, 'Missing required fields')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)', (name, email, phone))
        connection.commit()
        return jsonify({'message': 'Member added successfully'}), 201
    except Error as e:
        connection.rollback()
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

#get specific member
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT * FROM members WHERE id = %s', (id,))
        member = cursor.fetchone()
        if member:
            return jsonify(member)
        else:
            (404, 'Member not found')
    except Error as e:
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

#get all members
@app.route('/members', methods=['GET'])
def get_members():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        return jsonify(members)
    except Error as e:
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

#update a member
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    
    if not name or not email or not phone:
        (400, 'Missing required fields')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('UPDATE members SET name = %s, email = %s, phone = %s WHERE id = %s', (name, email, phone, id))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Member updated successfully'})
        else:
            (404, 'Member not found')
    except Error as e:
        connection.rollback()
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

#delete a member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('DELETE FROM members WHERE id = %s', (id,))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Member deleted successfully'})
        else:
            (404, 'Member not found')
    except Error as e:
        connection.rollback()
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

#Task 2: CRUD Operations session
#add session
@app.route('/sessions', methods=['POST'])
def schedule_session():
    data = request.get_json()
    member_id = data.get('member_id')
    date = data.get('date')
    workout_type = data.get('workout_type')
    
    if not member_id or not date or not workout_type:
        (400, 'Missing required fields')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('INSERT INTO workout_sessions (member_id, date, workout_type) VALUES (%s, %s, %s)', (member_id, date, workout_type))
        connection.commit()
        return jsonify({'message': 'Workout session scheduled successfully'}), 201
    except Error as e:
        connection.rollback()
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

#get all sessions for specific member
@app.route('/sessions/member/<int:member_id>', methods=['GET'])
def get_sessions_for_member(member_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT * FROM workout_sessions WHERE member_id = %s', (member_id,))
        sessions = cursor.fetchall()
        if sessions:
            return jsonify(sessions)
        else:
            (404, 'No workout sessions found for this member')
    except Error as e:
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()
#update session
@app.route('/sessions/<int:id>', methods=['PUT'])
def update_session(id):
    data = request.get_json()
    date = data.get('date')
    workout_type = data.get('workout_type')
    
    if not date or not workout_type:
        (400, 'Missing required fields')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('UPDATE workout_sessions SET date = %s, workout_type = %s WHERE id = %s', (date, workout_type, id))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Workout session updated successfully'})
        else:
            (404, 'Workout session not found')
    except Error as e:
        connection.rollback()
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

# Delete a workout session
@app.route('/sessions/<int:id>', methods=['DELETE'])
def delete_session(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('DELETE FROM workout_sessions WHERE id = %s', (id,))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Workout session deleted successfully'})
        else:
            (404, 'Workout session not found')
    except Error as e:
        connection.rollback()
        (500, f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
