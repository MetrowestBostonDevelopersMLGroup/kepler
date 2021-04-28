"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint, current_app, flash, redirect
from appManagement import session as sess
import argparse
import os
from werkzeug.utils import secure_filename
from appManagement import configMgr as cmgr

from validate_email import validate_email

KEPLER_API = Blueprint('kepler_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return KEPLER_API


@KEPLER_API.route('/v1/configuration', methods=['GET'])
def get_configurations():
    """Return all loaded configurations
    @return: 200: an array of all configurations as a \
    flask/response object with application/json mimetype.
    """
    return jsonify(current_app.appMethods.listUploadedConfigurations())

@KEPLER_API.route('/v1/session', methods=['POST'])
def get_session():
    """Creates and returns a unique session identifier
    @return: 200: a UUID identifying the session handle
    """    
    newConfigMgr = cmgr.ConfigMgr(os.getcwd()+current_app.config['UPLOAD_FOLDER'])
    sessionObj = sess.Session(newConfigMgr)
    sid = sessionObj.getNewSID()
    current_app.sessions[sid] = sessionObj
    return jsonify(sid)

@KEPLER_API.route('/v1/session', methods=['GET'])
def get_sessions():
    """Return all active sessions
    @return: 200: an array of all sessions as a \
    flask/response object with application/json mimetype.
    """
    return jsonify(current_app.sessions)


@KEPLER_API.route('/v1/loadAndParseConfig', methods=['POST'])
def loadAndParseConfig():
    """Load and parse a recommender config
    @param sessionId: post : a valid session identifier
    @param configFilename: post : the name of the configuration file to load and parse
    @return: 201: the parse output as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('filename'):
        abort(400)
    if not data.get('sessionId'):
        abort(400)

    response = current_app.appMethods.loadAndParseInSession(data['sessionId'], data['filename'])
    return response

@KEPLER_API.route('/v1/configRecommend', methods=['POST'])
def configRecommend():
    """Load and parse a recommender config
    @param sessionId: post : a valid session identifier
    @param prompt: post : the user specified text on which to base recommendations
    @return: 201: the parse output as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('prompt'):
        abort(400)
    if not data.get('sessionId'):
        abort(400)

    response = current_app.appMethods.configRecommend(data['sessionId'], data['prompt'])
    return response

