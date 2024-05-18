from flask import Blueprint, request, jsonify
import sqlite3
from Foods.foodsQueries import (
    CREATE_FOODS_TABLE, SELECT_ALL_FOODS, SELECT_FOOD_BY_ID,
    SELECT_FOOD_BY_NAME, INSERT_FOOD, CHECK_DUPLICATE_FOOD, UPDATE_FOOD_BY_ID,
    SEARCH_FOODS_BY_NAME
)

foods_bp = Blueprint('foods', __name__)

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
    execute_query(CREATE_FOODS_TABLE)

@foods_bp.route('/', methods=['GET'])
def get_foods():
    rows = fetch_query(SELECT_ALL_FOODS)
    
    foods = []
    for row in rows:
        food = {
            'Id': row[0],
            'Name': row[1],
            'PortionSize': row[2],
            'Calories': row[3],
            'TotalFat': row[4],
            'SaturatedFat': row[5],
            'Sodium': row[6],
            'TotalCarbs': row[7],
            'DietaryFiber': row[8],
            'Sugars': row[9],
            'Proteins': row[10],
            'Cholesterol': row[11]
        }
        foods.append(food)
    
    return jsonify(foods)

@foods_bp.route('/', methods=['POST'])
def add_food():
    data = request.get_json()
    name = data['Name']

    # Check for duplicate food by name
    duplicate_food = fetch_query(CHECK_DUPLICATE_FOOD, (name,))
    if duplicate_food:
        return jsonify({"error": "Food with the same name already exists!"}), 409

    # Convert Sodium and Cholesterol from mg to g before storing
    sodium_in_g = data['Sodium'] / 1000
    cholesterol_in_g = data['Cholesterol'] / 1000

    execute_query(INSERT_FOOD, (
        data['Name'], data['PortionSize'], data['Calories'], data['TotalFat'],
        data['SaturatedFat'], sodium_in_g, data['TotalCarbs'], data['DietaryFiber'],
        data['Sugars'], data['Proteins'], cholesterol_in_g
    ))
    return jsonify({"message": "Food added successfully!"}), 201

@foods_bp.route('/<int:id>', methods=['GET'])
def get_food_by_id(id):
    rows = fetch_query(SELECT_FOOD_BY_ID, (id,))
    if rows:
        row = rows[0]
        food = {
            'Id': row[0],
            'Name': row[1],
            'PortionSize': row[2],
            'Calories': row[3],
            'TotalFat': row[4],
            'SaturatedFat': row[5],
            'Sodium': row[6],
            'TotalCarbs': row[7],
            'DietaryFiber': row[8],
            'Sugars': row[9],
            'Proteins': row[10],
            'Cholesterol': row[11]
        }
        return jsonify(food)
    else:
        return jsonify({"message": "Food not found"}), 404

@foods_bp.route('/name/<string:name>', methods=['GET'])
def get_food_by_name(name):
    rows = fetch_query(SELECT_FOOD_BY_NAME, (name,))
    if rows:
        foods = []
        for row in rows:
            food = {
                'Id': row[0],
                'Name': row[1],
                'PortionSize': row[2],
                'Calories': row[3],
                'TotalFat': row[4],
                'SaturatedFat': row[5],
                'Sodium': row[6],
                'TotalCarbs': row[7],
                'DietaryFiber': row[8],
                'Sugars': row[9],
                'Proteins': row[10],
                'Cholesterol': row[11]
            }
            foods.append(food)
        return jsonify(foods)
    else:
        return jsonify({"message": "Food not found"}), 404

@foods_bp.route('/<int:id>', methods=['PUT'])
def update_food_by_id(id):
    data = request.get_json()

    # Convert Sodium and Cholesterol from mg to g before storing
    sodium_in_g = data['Sodium'] / 1000
    cholesterol_in_g = data['Cholesterol'] / 1000

    execute_query(UPDATE_FOOD_BY_ID, (
        data['Name'], data['PortionSize'], data['Calories'], data['TotalFat'],
        data['SaturatedFat'], sodium_in_g, data['TotalCarbs'], data['DietaryFiber'],
        data['Sugars'], data['Proteins'], cholesterol_in_g, id
    ))
    return jsonify({"message": "Food updated successfully!"}), 200

@foods_bp.route('/search', methods=['GET'])
def search_foods():
    query = request.args.get('q', '')
    if query:
        search_term = f"%{query}%"
        rows = fetch_query(SEARCH_FOODS_BY_NAME, (search_term,))
        results = [{'Id': row[0], 'Name': row[1]} for row in rows]
        return jsonify(results)
    else:
        return jsonify({"message": "No search query provided"}), 400

# Initialize the database when the module is imported
initialize_database()
