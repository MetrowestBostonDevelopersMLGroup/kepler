from flask import Flask
from flask import render_template
import json

import argparse
import os
from flask import jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api
from recommend import prepdata, movies
from appManagement import session

# git push origin main

app = Flask(__name__)
app.session = {'session1': session.Session(None, None, None)}

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

app.register_blueprint(request_api.get_blueprint())

@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


@app.route("/")
def hello():
    print("hello world")
    return app.send_static_file("index.html")

@app.route('/hello')
def hello_world():
   return "hello world"


# index route
# params
@app.route("/products")
def index():
    with open('data/products.json') as f:
        data = json.load(f)
 
    prepdata.load_data()

    return render_template('index.html', products=data)

@app.route("/load")
def load():    
    app.session['session1'].dataPrep = prepdata.load_data()
    return app.session['session1'].dataPrep.head(3).to_html()

@app.route("/describe")
def describe():    
    #app.session['session1'].dataTransform = prepdata.describe_data(app.session['session1'].dataPrep)
    #return app.session['session1'].dataTransform.head(3).to_html()
    return 'not implemented'

@app.route("/transform")
def transform():    
    app.session['session1'].dataTransform = movies.transform_data(app.session['session1'].dataPrep)
    return "data ready"

#@app.route('/recommend/<string:movie_title>', methods=['GET'])
@app.route("/recommend")
def recommend():    #movie_title
    movie_title = "Jaws"
    data = movies.recommend_movies(movie_title, app.session['session1'].dataPrep, app.session['session1'].dataTransform)
    return data

@app.route("/all")
def all():    #movie_title
    load()
    transform()
    data = recommend()
    return data.to_html()


if __name__ == "__main__":
    app.run(debug=True)
