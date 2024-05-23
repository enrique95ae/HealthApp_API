from flask import Blueprint, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from Users.usersQueries import (
    CREATE_USERS_TABLE, SELECT_ALL_USERS, SELECT_USER_BY_ID,
    SELECT_USER_BY_USERNAME, INSERT_USER, UPDATE_USER_BY_ID,
    CREATE_USER_WEIGHT_TABLE, INSERT_USER_WEIGHT, SELECT_USER_WEIGHTS, CHECK_TODAYS_WEIGHT_ENTRY
)

users_bp = Blueprint('users', __name__)

# Function to execute SQL queries
def execute_query(query, args=()):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()

# Function to fetch data from the database
def fetch_query(query, args=()):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return rows

# Initialize the database
def initialize_database():
    execute_query(CREATE_USERS_TABLE)
    execute_query(CREATE_USER_WEIGHT_TABLE)

@users_bp.route('/', methods=['GET'])
def get_users():
    rows = fetch_query(SELECT_ALL_USERS)
    
    users = []
    for row in rows:
        user = {
            'Id': row[0],
            'Name': row[1],
            'DoB': row[2],
            'Weight': row[3],
            'Height': row[4],
            'BodyType': row[5],
            'Goal': row[6],
            'Username': row[7]
        }
        users.append(user)
    
    return jsonify(users)

@users_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['Username']

    # Check for duplicate user by username
    duplicate_user = fetch_query(SELECT_USER_BY_USERNAME, (username,))
    if duplicate_user:
        return jsonify({"error": "User with the same username already exists!"}), 409

    # Hash the password before storing
    hashed_password = generate_password_hash(data['Password'], method='pbkdf2:sha256')

    execute_query(INSERT_USER, (
        data['Name'], data['DoB'], data['Weight'], data['Height'],
        data['BodyType'], data['Goal'], username, hashed_password
    ))
    return jsonify({"message": "User added successfully!"}), 201

@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    rows = fetch_query(SELECT_USER_BY_ID, (id,))
    if rows:
        row = rows[0]
        user = {
            'Id': row[0],
            'Name': row[1],
            'DoB': row[2],
            'Weight': row[3],
            'Height': row[4],
            'BodyType': row[5],
            'Goal': row[6],
            'Username': row[7]
        }
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    data = request.get_json()

    # Hash the password before storing
    hashed_password = generate_password_hash(data['Password'], method='pbkdf2:sha256')

    execute_query(UPDATE_USER_BY_ID, (
        data['Name'], data['DoB'], data['Weight'], data['Height'],
        data['BodyType'], data['Goal'], data['Username'], hashed_password, id
    ))
    return jsonify({"message": "User updated successfully!"}), 200

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    
    if not data or 'Username' not in data or 'Password' not in data:
        return jsonify({"error": "Username and Password are required"}), 400

    username = data['Username']
    password = data['Password']

    # Fetch user by username
    user = fetch_query(SELECT_USER_BY_USERNAME, (username,))
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    user = user[0]
    # Check the password
    if check_password_hash(user[8], password):  # Assuming password is the 9th column
        user_data = {
            'Id': user[0],
            'Name': user[1],
            'DoB': user[2],
            'Weight': user[3],
            'Height': user[4],
            'BodyType': user[5],
            'Goal': user[6],
            'Username': user[7]
        }
        return jsonify(user_data)
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# Weight-related endpoints
@users_bp.route('/weights', methods=['POST'])
def add_user_weight():
    data = request.get_json()
    user_id = data['USER_Id']
    weight = data['Weight']
    entry_date = datetime.now().strftime("%Y-%m-%d")

    execute_query(INSERT_USER_WEIGHT, (user_id, entry_date, weight))
    return jsonify({"message": "Weight entry added successfully!"}), 201

@users_bp.route('/weights/<int:user_id>', methods=['GET'])
def get_user_weights(user_id):
    weights = fetch_query(SELECT_USER_WEIGHTS, (user_id,))
    weight_list = []
    for weight in weights:
        weight_item = {
            'Id': weight[0],
            'USER_Id': weight[1],
            'EntryDate': weight[2],
            'Weight': weight[3]
        }
        weight_list.append(weight_item)
    return jsonify(weight_list)

@users_bp.route('/weights/today/<int:user_id>', methods=['GET'])
def check_weight_today(user_id):
    today_date = datetime.now().strftime("%Y-%m-%d")
    result = fetch_query(CHECK_TODAYS_WEIGHT_ENTRY, (user_id, today_date))
    weight_entered = result[0][0] > 0
    return jsonify({"date": today_date, "weight_entered": weight_entered})

# Initialize the database when the module is imported
initialize_database()
