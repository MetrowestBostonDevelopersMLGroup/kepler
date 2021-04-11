from flask import Flask
from flask import render_template, flash, request, redirect, url_for
import json, pathlib

import argparse
import os
from flask import jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from routes import kepler_api
from recommend import prepdata, movies
from appManagement import session
from appManagement import configMgr as cmgr
from engine import engine as eng
from werkzeug.utils import secure_filename

# git push origin main

UPLOAD_FOLDER = '/upload'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'cfg'}


app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'memcached'
#sess.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.sessions = []

# create a single session for all interaction (when developing locally)
app.session = {'session1': session.Session(None, None, None)}

app.current_editor_file_id = None
app.current_filename = None
app.current_filename_basename = None
app.parseError = None
app.readyToRecommendMessage = None
app.current_config = None
app.current_requestColumn = None
app.current_searchValue = None
app.recEngine = None

app.configMgr = cmgr.ConfigMgr(os.getcwd()+app.config['UPLOAD_FOLDER'])

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

app.register_blueprint(kepler_api.get_blueprint())

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

    return render_template('recommend.html', products=data)

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
    movie_title = "The Sting"
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
    result = recEngine.Recommendation('Aliens')
    return result.to_html()    
    #return config.GetAudit().MessagesAsHtmlTable()  #aud as json

@app.route("/loadindianmoviesconfig")
def loadIndianMoviesConfig():    #movie_title
    config = cmgr.ConfigMgr(os.getcwd()+app.config['UPLOAD_FOLDER'])
    res = config.LoadAndParse('./documentation/indian_movies_db_config.json') 
    aud = config.ValidateConfig()    
    recEngine = eng.Engine(config)
    recEngine.Execute() 
    result = recEngine.Recommendation('Amavas')
    return result.to_html()    
    #return config.GetAudit().MessagesAsHtmlTable()  #aud as json


@app.route('/editconfig', methods=['GET', 'POST'])
def editconfig_file():
    if request.method == 'POST':
        # check if the post request has the file part
        #if 'file' not in request.files:
        #    flash('No file part')
        #    return redirect(request.url)
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
    
    with open('./documentation/us_movies_db_config.json') as f:
        content = f.read()
    parsed_json = json.loads(content)
    data = {'config':content}
    return render_template('configeditor.html', editor=data)

@app.route("/config_editor", methods=['GET', 'POST'])
def cfg_editor():
    if request.method == 'POST':    
        if request.form['files'] != app.current_editor_file_id:
            # open up the file that is selected
            app.current_filename = app.config_files[int (request.form['files'])-1]['name']
            app.current_filename_basename = os.path.basename(app.current_filename)
            filename = os.getcwd()+app.config['UPLOAD_FOLDER']+'/'+ app.current_filename
            with open(filename) as f:
                content = f.read()
                parsed_json = json.loads(content)
            app.current_editor_file_id = request.form['files']
            app.current_filename = filename
            data = {'filename':app.current_filename,'config':content, 'files':app.config_files, 'audit':'', 'file_basename':app.current_filename_basename}
            return render_template('configeditor.html', editor=data)
        else:
            # save and parse the existing file
            content, isParsed = app.configMgr.Parse(request.form['editor'])
            if isParsed == True and app.current_filename_basename and allowed_file(app.current_filename_basename):
                filename = secure_filename(app.current_filename_basename)
                updir = os.getcwd()+app.config['UPLOAD_FOLDER']
                file = open(os.path.join(updir, app.current_filename_basename), 'w')
                file.write(content)
                file.close()

            audit = json.dumps(app.configMgr.GetAudit(), indent = 4, default=lambda o: o.__dict__)
            if request.form.get('nowarnings') != None:
                audit = [x for x in app.configMgr.GetAudit() if x.level == 'Error']
                audit = json.dumps(app.configMgr.GetAudit(), indent = 4, default=lambda o: o.__dict__)
            data = {'filename':app.current_filename,'config':content, 'files':app.config_files, 'audit':audit, 'file_basename':app.current_filename_basename}
            return render_template('configeditor.html', editor=data)

    content = ''
    filename = ''
    app.current_editor_file_id = None
    app.current_filename = None
    app.current_filename_basename = None
    app.current_requestColumn = None
    app.parseError = None
    app.current_config = None
    app.recEngine = None
    app.current_searchValue = None

    updir = os.getcwd()+app.config['UPLOAD_FOLDER']
    os.makedirs(updir, exist_ok=True)  
    files = os.listdir(updir)

    app.config_files = []
    id = 1
    for f in files:
        file_extension = pathlib.Path(f).suffix
        if (file_extension == '.cfg'):
            app.config_files.append({'id':id,'name':f})
            id = id +1

    data = {'filename':filename,'config':content, 'files':app.config_files}
    return render_template('configeditor.html', editor=data)

@app.route("/recommender", methods=['GET', 'POST'])
def recommender():
    if request.method == 'POST':    
        if request.form['files'] != app.current_editor_file_id:
            # open up the file that is selected
            app.current_filename = app.config_files[int (request.form['files'])-1]['name']
            app.current_filename_basename = os.path.basename(app.current_filename)
            filename = os.getcwd()+app.config['UPLOAD_FOLDER']+'/'+ app.current_filename
            app.current_editor_file_id = request.form['files']
            app.current_filename = filename

            app.current_config = cmgr.ConfigMgr(os.getcwd()+app.config['UPLOAD_FOLDER'])
            content, isParsed = app.current_config.LoadAndParse(filename) 
            app.parseError = app.current_config.IsAuditError()
            if app.parseError is not True:
                app.recEngine = eng.Engine(app.current_config)
                app.recEngine.Execute() 
                app.current_requestColumn = app.current_config.GetRequestColumnName()
                app.readyToRecommendMessage = 'Configuration is parsed without errors. The analysis is complete. Ready to recommend!'
            else:
                app.readyToRecommendMessage = 'Configuration is parsed with errors. The analysis can not proceed complete and recommendations can not be made.'

            data = {'filename':app.current_filename,'config':content, 'files':app.config_files, 'audit':'', 'file_basename':app.current_filename_basename, 'parse_error':app.readyToRecommendMessage , 'tables':[],'titles':[], 'requestColumn': app.current_requestColumn,'searchValue':'' }
            return render_template('recommend.html', recommend=data)
        else:
            # try a recommendation
            prompt = request.form.get('userinput')
            app.current_searchValue = prompt
            result, isRecommendSuccess = app.recEngine.Recommendation(prompt)
            resulthtml = result.to_html()  
            numpy = result.to_numpy() 
            asstring =  result.to_string().replace('\n','<br>')
            data = {'filename':app.current_filename,'config':'', 'files':app.config_files, 'audit':'', 'file_basename':app.current_filename_basename, 'parse_error':app.readyToRecommendMessage, 'tables':[result.to_html(classes='data')], 'titles':result.columns.values, 'requestColumn': app.current_requestColumn, 'searchValue':app.current_searchValue}
            return render_template('recommend.html', recommend=data)

    content = ''
    filename = ''
    app.current_editor_file_id = None
    app.current_filename = None
    app.current_filename_basename = None
    app.parseError = None
    app.current_config = None
    app.current_requestColumn = None
    app.current_searchValue = None
    app.recEngine = None
    updir = os.getcwd()+app.config['UPLOAD_FOLDER']
    os.makedirs(updir, exist_ok=True)  
    files = os.listdir(updir)
    app.config_files = []
    id = 1
    for f in files:
        file_extension = pathlib.Path(f).suffix
        if (file_extension == '.cfg'):
            app.config_files.append({'id':id,'name':f})
            id = id +1

    data = {'filename':filename,'config':content, 'files':app.config_files, 'tables':[],'titles':[], 'requestColumn': '','searchValue':''}
    return render_template('recommend.html', recommend=data)

if __name__ == "__main__":
    app.run(debug=True)
