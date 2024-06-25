import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from Foods.foods import foods_bp
from Users.users import users_bp
from Foods.meals import meals_bp
from Workouts.workouts import workouts_bp 
from CaloricIntake.caloricIntake import caloric_intake_bp

app = Flask(__name__)
CORS(app)  
app.register_blueprint(foods_bp, url_prefix='/foods')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(meals_bp, url_prefix='/meals')
app.register_blueprint(caloric_intake_bp, url_prefix='/users')
app.register_blueprint(workouts_bp, url_prefix='/workouts')



logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.errorhandler(403)
def forbidden_error(error):
    app.logger.error('Forbidden error: %s', error)
    return jsonify({'error': 'Forbidden'}), 403

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('Not found error: %s', error)
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Internal server error: %s', error)
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)