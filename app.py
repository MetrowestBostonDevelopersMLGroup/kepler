from flask import Flask
from flask import render_template
import json

import argparse
import os
from flask import jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

## swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Recommender-System-Python-Flask-REST"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# index route
# params
@app.route("/")
def index():
    with open('data/products.json') as f:
        data = json.load(f)
 
    return render_template('index.html', products=data)


if __name__ == "__main__":
    app.run(debug=True)
