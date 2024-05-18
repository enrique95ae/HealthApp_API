from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
from Foods.mealsQueries import (
    CREATE_USR_MEAL_TABLE, CREATE_MEAL_FOODS_TABLE,
    SELECT_MEALS_BY_USER_TODAY, SELECT_FOODS_BY_MEAL
)

meals_bp = Blueprint('meals', __name__)

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
    execute_query(CREATE_USR_MEAL_TABLE)
    execute_query(CREATE_MEAL_FOODS_TABLE)

@meals_bp.route('/usr_meals', methods=['POST'])
def add_usr_meal():
    data = request.get_json()
    user_id = data['USER_Id']
    creation_date = datetime.now().strftime("%Y-%m-%d")
    creation_time = datetime.now().strftime("%I:%M %p").split(' ')[0]
    hour_period = datetime.now().strftime("%I:%M %p").split(' ')[1]
    title = data['Title']
    score = data['Score']

    execute_query("INSERT INTO USR_MEAL (USER_Id, CreationDate, CreationTime, HourPeriod, Title, Score) VALUES (?, ?, ?, ?, ?, ?)",
                  (user_id, creation_date, creation_time, hour_period, title, score))
    return jsonify({"message": "User meal added successfully!"}), 201

@meals_bp.route('/meal_foods', methods=['POST'])
def add_meal_food():
    data = request.get_json()
    usr_meal_id = data['USR_MEAL_ID']
    foods_id = data['FOODS_ID']
    portion_eaten = data['portionEaten']

    execute_query("INSERT INTO MEAL_FOODS (USR_MEAL_ID, FOODS_ID, portionEaten) VALUES (?, ?, ?)", (usr_meal_id, foods_id, portion_eaten))
    return jsonify({"message": "Meal food added successfully!"}), 201

@meals_bp.route('/meals_today/<int:user_id>', methods=['GET'])
def get_meals_today(user_id):
    # Compute the current date in YYYY-MM-DD format
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Fetch meals for the user for today
    meals = fetch_query(SELECT_MEALS_BY_USER_TODAY, (user_id, today_date + '%'))
    print(f"Meals for user {user_id} today: {meals}")  # Debug print
    
    meals_list = []
    for meal in meals:
        meal_id, creation_date, creation_time, hour_period, title, score = meal
        # Fetch foods for each meal
        foods = fetch_query(SELECT_FOODS_BY_MEAL, (meal_id,))
        print(f"Foods for meal {meal_id}: {foods}")  # Debug print
        
        foods_list = []
        for food in foods:
            food_item = {
                'Id': food[0],
                'Name': food[1],
                'PortionSize': food[2],
                'Calories': food[3],
                'TotalFat': food[4],
                'SaturatedFat': food[5],
                'Sodium': food[6],
                'TotalCarbs': food[7],
                'DietaryFiber': food[8],
                'Sugars': food[9],
                'Proteins': food[10],
                'Cholesterol': food[11],
                'PortionEaten': food[12]
            }
            foods_list.append(food_item)
        
        meal_item = {
            'Id': meal_id,
            'CreationDate': creation_date,
            'CreationTime': creation_time,
            'HourPeriod': hour_period,
            'Title': title,
            'Score': score,
            'Foods': foods_list
        }
        meals_list.append(meal_item)
    
    return jsonify(meals_list)

# Initialize the database when the module is imported
initialize_database()
