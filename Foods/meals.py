from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
from Foods.mealsQueries import (
    CREATE_USR_MEAL_TABLE, CREATE_MEAL_FOODS_TABLE, SELECT_MEAL_BY_ID,
    SELECT_MEALS_BY_USER_TODAY, SELECT_FOODS_BY_MEAL, SELECT_USER_MEALS_PAGINATED, SELECT_TOTAL_MEALS_COUNT
)

meals_bp = Blueprint('meals', __name__)


def execute_query(query, args=()):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    last_row_id = cur.lastrowid
    conn.close()
    return last_row_id


def fetch_query(query, args=()):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return rows


def initialize_database():
    execute_query(CREATE_USR_MEAL_TABLE)
    execute_query(CREATE_MEAL_FOODS_TABLE)


def paginate_query(base_query, page, page_size, args=()):
    offset = (page - 1) * page_size
    paginated_query = base_query + " LIMIT ? OFFSET ?"
    return fetch_query(paginated_query, args + (page_size, offset))

@meals_bp.route('/usr_meals', methods=['POST'])
def add_usr_meal():
    data = request.get_json()
    user_id = data['USER_Id']
    creation_date = datetime.now().strftime("%Y-%m-%d")
    creation_time_period = data['CreationTime']
    
    
    creation_time = datetime.strptime(creation_time_period, "%I:%M%p").strftime("%I:%M")
    hour_period = datetime.strptime(creation_time_period, "%I:%M%p").strftime("%p")

    title = data['Title']
    score = data['Score']

    meal_id = execute_query("INSERT INTO USR_MEAL (USER_Id, CreationDate, CreationTime, HourPeriod, Title, Score) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id, creation_date, creation_time, hour_period, title, score))
    return jsonify({"message": "User meal added successfully!", "Id": meal_id}), 201

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
    
    today_date = datetime.now().strftime("%Y-%m-%d")

    
    meals = fetch_query(SELECT_MEALS_BY_USER_TODAY, (user_id, today_date + '%'))
    print(f"Meals for user {user_id} today: {meals}")  
    
    meals_list = []
    for meal in meals:
        meal_id, creation_date, creation_time, hour_period, title, score = meal
        
        formatted_creation_time = f"{creation_time} {hour_period}"
        
        foods = fetch_query(SELECT_FOODS_BY_MEAL, (meal_id,))
        print(f"Foods for meal {meal_id}: {foods}")  
        
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
            'CreationTime': formatted_creation_time,
            'Title': title,
            'Score': score,
            'Foods': foods_list
        }
        meals_list.append(meal_item)
    
    return jsonify(meals_list)

@meals_bp.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal_by_id(meal_id):
    
    meal = fetch_query(SELECT_MEAL_BY_ID, (meal_id,))
    print(f"Meal details for meal {meal_id}: {meal}")  
    if not meal:
        return jsonify({"message": "Meal not found"}), 404
    
    meal = meal[0]
    meal_details = {
        'Id': meal[0],
        'USER_Id': meal[1],
        'CreationDate': meal[2],
        'CreationTime': f"{meal[3]} {meal[4]}",  
        'Title': meal[5],
        'Score': meal[6]
    }
    
    
    foods = fetch_query(SELECT_FOODS_BY_MEAL, (meal_id,))
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
    
    meal_details['Foods'] = foods_list
    return jsonify(meal_details)

@meals_bp.route('/user_meals/<int:user_id>', methods=['GET'])
def get_user_meals(user_id):
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)

    
    total_meals = fetch_query(SELECT_TOTAL_MEALS_COUNT, (user_id,))[0][0]
    total_pages = (total_meals + page_size - 1) // page_size

    meals = paginate_query(SELECT_USER_MEALS_PAGINATED, page, page_size, (user_id,))
    
    items = []
    for meal in meals:
        meal_id = meal[0]
        meal_details = {
            'Id': meal_id,
            'Title': meal[2],
            'Score': meal[3],
            'CreationDate': meal[4],
            'CreationTime': f"{meal[5]} {meal[6]}",
            'Foods': []
        }
        
        
        foods = fetch_query(SELECT_FOODS_BY_MEAL, (meal_id,))
        for food in foods:
            food_details = {
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
            meal_details['Foods'].append(food_details)
        
        items.append(meal_details)
    
    response = {
        'items': items,
        'totalPages': total_pages
    }
    
    return jsonify(response)


initialize_database()