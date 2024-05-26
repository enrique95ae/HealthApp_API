import sqlite3
from datetime import datetime

DATABASE = 'database.db'  # Ensure this path is correct

def fetch_query(query, args=()):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_user_data(user_id):
    query = "SELECT Gender, (strftime('%Y', 'now') - strftime('%Y', DoB)) as age, Weight, Height, Goal, BodyType FROM USERS WHERE Id = ?"
    user_data = fetch_query(query, (user_id,))
    
    if not user_data:
        raise ValueError("User not found")
    
    user = user_data[0]
    return {
        "gender": user[0],
        "age": user[1],
        "weight": user[2],
        "height": user[3],
        "goal": user[4],
        "body_type": user[5]
    }

def calculateUserBMR(user_id):
    user_data = get_user_data(user_id)
    
    gender = user_data['gender']
    age = user_data['age']
    weight = user_data['weight']
    height = user_data['height']
    goal = user_data['goal']
    
    if gender == 'male':
        bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
    else:  # female
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
    
    if goal == 'lose weight':
        bmr -= 500
    elif goal == 'gain muscle':
        bmr += 500
    # No adjustment needed for 'maintain'

    return round(bmr)

def get_macros_today(user_id):
    today_date = datetime.now().strftime("%Y-%m-%d")
    query = """
    SELECT F.TotalFat, F.Proteins, F.TotalCarbs, MF.portionEaten
    FROM USR_MEAL UM
    JOIN MEAL_FOODS MF ON UM.Id = MF.USR_MEAL_ID
    JOIN FOODS F ON MF.FOODS_ID = F.Id
    WHERE UM.USER_Id = ? AND UM.CreationDate = ?
    """
    meals_data = fetch_query(query, (user_id, today_date))
    
    total_consumed_fat = 0
    total_consumed_protein = 0
    total_consumed_carbs = 0
    
    for meal in meals_data:
        fat, protein, carbs, portion_eaten = meal
        total_consumed_fat += (fat)
        total_consumed_protein += (protein)
        total_consumed_carbs += (carbs)
    
    user_data = get_user_data(user_id)
    bmr = calculateUserBMR(user_id)
    
    if user_data["body_type"] == "Endomorph":
        total_carbs = round(bmr * 0.25 / 4)
        total_protein = round(bmr * 0.40 / 4)
        total_fat = round(bmr * 0.35 / 9)
    elif user_data["body_type"] == "Mesomorph":
        total_carbs = round(bmr * 0.35 / 4)
        total_protein = round(bmr * 0.35 / 4)
        total_fat = round(bmr * 0.30 / 9)
    elif user_data["body_type"] == "Ectomorph":
        total_carbs = round(bmr * 0.40 / 4)
        total_protein = round(bmr * 0.30 / 4)
        total_fat = round(bmr * 0.30 / 9)
    else:
        raise ValueError("Unknown body type")
    
    return {
        "totalCalories": bmr,
        "totalFat": total_fat,
        "totalProtein": total_protein,
        "totalCarbs": total_carbs,
        "consumedFat": round(total_consumed_fat),
        "consumedProtein": round(total_consumed_protein),
        "consumedCarbs": round(total_consumed_carbs)
    }
