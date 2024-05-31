from flask import Blueprint, request, jsonify
import sqlite3
from .workoutsQueries import (
    CREATE_EXERCISES_TABLE, CREATE_EXERCISE_SETS_TABLE, CREATE_WORKOUTS_TABLE, CREATE_WORKOUT_EXERCISE_SETS_TABLE,
    SELECT_ALL_EXERCISES, SELECT_EXERCISE_BY_ID, INSERT_EXERCISE,
    SELECT_ALL_EXERCISE_SETS, SELECT_EXERCISE_SET_BY_ID, INSERT_EXERCISE_SET,
    SELECT_ALL_WORKOUTS, SELECT_WORKOUT_BY_ID, INSERT_WORKOUT,
    SELECT_ALL_WORKOUT_EXERCISE_SETS, SELECT_WORKOUT_EXERCISE_SET_BY_ID, INSERT_WORKOUT_EXERCISE_SET,
    UPDATE_WORKOUT_BY_ID, SELECT_WORKOUT_DETAILS
)

workouts_bp = Blueprint('workouts', __name__)

# Function to execute SQL queries
def execute_query(query, args=()):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    last_row_id = cur.lastrowid
    conn.close()
    return last_row_id

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
    execute_query(CREATE_EXERCISES_TABLE)
    execute_query(CREATE_EXERCISE_SETS_TABLE)
    execute_query(CREATE_WORKOUTS_TABLE)
    execute_query(CREATE_WORKOUT_EXERCISE_SETS_TABLE)

@workouts_bp.route('/exercises', methods=['GET'])
def get_exercises():
    rows = fetch_query(SELECT_ALL_EXERCISES)
    exercises = []
    for row in rows:
        exercise = {
            'Id': row[0],
            'Name': row[1],
            'Type': row[2],
            'Muscle': row[3],
            'Equipment': row[4],
            'Difficulty': row[5],
            'Instructions': row[6]
        }
        exercises.append(exercise)
    return jsonify(exercises)

@workouts_bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    rows = fetch_query(SELECT_EXERCISE_BY_ID, (id,))
    if rows:
        row = rows[0]
        exercise = {
            'Id': row[0],
            'Name': row[1],
            'Type': row[2],
            'Muscle': row[3],
            'Equipment': row[4],
            'Difficulty': row[5],
            'Instructions': row[6]
        }
        return jsonify(exercise)
    else:
        return jsonify({"message": "Exercise not found"}), 404

@workouts_bp.route('/exercises', methods=['POST'])
def add_exercise():
    data = request.get_json()
    execute_query(INSERT_EXERCISE, (
        data['Name'], data['Type'], data['Muscle'], data['Equipment'],
        data['Difficulty'], data['Instructions']
    ))
    return jsonify({"message": "Exercise added successfully!"}), 201

@workouts_bp.route('/exercise_sets', methods=['GET'])
def get_exercise_sets():
    rows = fetch_query(SELECT_ALL_EXERCISE_SETS)
    exercise_sets = []
    for row in rows:
        exercise_set = {
            'Id': row[0],
            'Exercise_Id': row[1],
            'Sets': row[2],
            'Reps': row[3],
            'SetOrder': row[4]
        }
        exercise_sets.append(exercise_set)
    return jsonify(exercise_sets)

@workouts_bp.route('/exercise_sets/<int:id>', methods=['GET'])
def get_exercise_set_by_id(id):
    rows = fetch_query(SELECT_EXERCISE_SET_BY_ID, (id,))
    if rows:
        row = rows[0]
        exercise_set = {
            'Id': row[0],
            'Exercise_Id': row[1],
            'Sets': row[2],
            'Reps': row[3],
            'SetOrder': row[4]
        }
        return jsonify(exercise_set)
    else:
        return jsonify({"message": "Exercise set not found"}), 404

@workouts_bp.route('/exercise_sets', methods=['POST'])
def add_exercise_set():
    data = request.get_json()
    execute_query(INSERT_EXERCISE_SET, (
        data['Exercise_Id'], data['Sets'], data['Reps'], data['SetOrder']
    ))
    return jsonify({"message": "Exercise set added successfully!"}), 201

@workouts_bp.route('/workouts', methods=['GET'])
def get_workouts():
    rows = fetch_query(SELECT_ALL_WORKOUTS)
    workouts = []
    for row in rows:
        workout = {
            'Id': row[0],
            'Title': row[1],
            'Color': row[2],
            'Type': row[3],
            'Description': row[4]
        }
        workouts.append(workout)
    return jsonify(workouts)

@workouts_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    rows = fetch_query(SELECT_WORKOUT_BY_ID, (id,))
    if rows:
        row = rows[0]
        workout = {
            'Id': row[0],
            'Title': row[1],
            'Color': row[2],
            'Type': row[3],
            'Description': row[4]
        }
        return jsonify(workout)
    else:
        return jsonify({"message": "Workout not found"}), 404

@workouts_bp.route('/workouts', methods=['POST'])
def add_workout():
    data = request.get_json()
    execute_query(INSERT_WORKOUT, (
        data['Title'], data['Color'], data['Type'], data['Description']
    ))
    return jsonify({"message": "Workout added successfully!"}), 201

@workouts_bp.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    data = request.get_json()
    execute_query(UPDATE_WORKOUT_BY_ID, (
        data['Title'], data['Color'], data['Type'], data['Description'], id
    ))
    return jsonify({
        "Id": id,
        "Title": data['Title'],
        "Color": data['Color'],
        "Type": data['Type'],
        "Description": data['Description']
    }), 200

@workouts_bp.route('/workout_exercise_sets', methods=['GET'])
def get_workout_exercise_sets():
    rows = fetch_query(SELECT_ALL_WORKOUT_EXERCISE_SETS)
    workout_exercise_sets = []
    for row in rows:
        workout_exercise_set = {
            'Id': row[0],
            'Workout_Id': row[1],
            'Exercise_Id': row[2]
        }
        workout_exercise_sets.append(workout_exercise_set)
    return jsonify(workout_exercise_sets)

@workouts_bp.route('/workout_exercise_sets/<int:id>', methods=['GET'])
def get_workout_exercise_set_by_id(id):
    rows = fetch_query(SELECT_WORKOUT_EXERCISE_SET_BY_ID, (id,))
    if rows:
        row = rows[0]
        workout_exercise_set = {
            'Id': row[0],
            'Workout_Id': row[1],
            'Exercise_Id': row[2]
        }
        return jsonify(workout_exercise_set)
    else:
        return jsonify({"message": "Workout exercise set not found"}), 404

@workouts_bp.route('/workouts/<int:workout_id>/details', methods=['GET'])
def get_workout_details(workout_id):
    rows = fetch_query(SELECT_WORKOUT_DETAILS, (workout_id,))
    
    if not rows:
        return jsonify({"message": "Workout not found"}), 404
    
    workout = {
        'Id': rows[0][0],
        'Title': rows[0][1],
        'Color': rows[0][2],
        'Type': rows[0][3],
        'Description': rows[0][4],
        'Exercises': []
    }

    for row in rows:
        exercise = {
            'Id': row[5],
            'Name': row[6],
            'Type': row[7],
            'Muscle': row[8],
            'Equipment': row[9],
            'Difficulty': row[10],
            'Instructions': row[11],
            'Sets': row[12],
            'Reps': row[13],
            'SetOrder': row[14]
        }
        workout['Exercises'].append(exercise)
    
    return jsonify(workout)

# Initialize the database when the module is imported
initialize_database()
