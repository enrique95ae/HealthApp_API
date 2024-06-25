from flask import Blueprint, jsonify
from CaloricIntake.caloricIntakeQueries import calculateUserBMR, get_macros_today

caloric_intake_bp = Blueprint('caloric_intake', __name__)

@caloric_intake_bp.route('/bmr/<int:id>', methods=['GET'])
def get_user_bmr(id):
    try:
        bmr_result = calculateUserBMR(id)
        return jsonify({"bmr": bmr_result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@caloric_intake_bp.route('/macros_today/<int:id>', methods=['GET'])
def get_macros_today_endpoint(id):
    try:
        macros_result = get_macros_today(id)
        return jsonify(macros_result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400