import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from Foods.foods import foods_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.register_blueprint(foods_bp, url_prefix='/foods')

# Configure logging
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
    app.run()
