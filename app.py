from flask import Flask
from flask import render_template, flash, request, redirect, url_for
import json

import argparse
import os
from flask import jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api
from recommend import prepdata, movies
from appManagement import session
from appManagement import configMgr as cmgr
from engine import engine as eng
from werkzeug.utils import secure_filename

# git push origin main

UPLOAD_FOLDER = '/upload'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# create a single session for all interaction (when developing locally)
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
    app.session['session1'].dataTransform = movies.analyze(app.session['session1'].dataPrep)
    return "data ready"

#@app.route('/recommend/<string:movie_title>', methods=['GET'])
@app.route("/recommend")
def recommend():    #movie_title
    movie_title = "Alien"
    data = movies.recommend(movie_title, app.session['session1'].dataPrep, app.session['session1'].dataTransform)
    return data

@app.route("/all")
def all():    #movie_title
    load()
    transform()
    data = recommend()
    return data.to_html()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')            
            return redirect(request.url)
        updir = os.getcwd()+app.config['UPLOAD_FOLDER']
        os.makedirs(updir, exist_ok=True)             
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(updir, filename))
            return filename + ' has been uploaded.'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/loadsampleconfig")
def loadSampleConfig():    #movie_title
    config = cmgr.ConfigMgr(os.getcwd()+app.config['UPLOAD_FOLDER'])
    res = config.LoadAndParse('./documentation/sample_describe.json')
    aud = config.ValidateConfig()       
    return aud
    
@app.route("/loadusmoviesconfig")
def loadUSMoviesConfig():    #movie_title
    config = cmgr.ConfigMgr(os.getcwd()+app.config['UPLOAD_FOLDER'])
    res = config.LoadAndParse('./documentation/us_movies_db_config.json') #clean.json)
    aud = config.ValidateConfig()    
    recEngine = eng.Engine(config)
    recEngine.Execute()

    return aud    
    #return config.GetAudit().MessagesAsHtmlTable()  #aud as json


if __name__ == "__main__":
    app.run(debug=True)
