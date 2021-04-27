import os
import json, pathlib
from flask import jsonify
from engine import engine as eng

class AppMethods:

    sessions = None
    uploadFolder = None

    def __init__(self, sessions, uploadFolder):
        self.sessions = sessions
        self.uploadFolder = uploadFolder

    def loadAndParseInSession(self, sessionId, filename):
        session = self.sessions[sessionId]
        session.setFilename(filename)
        filename = os.getcwd()+self.uploadFolder+'/'+ filename
        content, isParsed = session.getConfigMgr().LoadAndParse(filename) 

        if (isParsed is True):
            recEngine = eng.Engine(session.getConfigMgr())
            session.setRecEngine(recEngine)
            recEngine.Execute() 

        return content

    def configRecommend(self, sessionId, prompt):
        session = self.sessions[sessionId]        
        result, isRecommendSuccess = session.getRecEngine().Recommendation(prompt)
        return result.to_json(orient="split")

    def listUploadedConfigurations(self):
        updir = os.getcwd()+self.uploadFolder
        os.makedirs(updir, exist_ok=True)  
        files = os.listdir(updir)

        config_files = []
        for f in files:
            file_extension = pathlib.Path(f).suffix
            if (file_extension == '.cfg'):
                config_files.append(f)

        return config_files