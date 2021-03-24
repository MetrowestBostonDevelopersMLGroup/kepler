import pandas as pd
import json
from appManagement import dataFile as df
from appManagement import audit as au

class ConfigMgr:
    
    parsed_json = None
    filesObj = []
    uploadFolder = None
    audit = None

    def __init__(self, uploadFolder):
        self.uploadFolder = uploadFolder
        self.audit = au.Audit()

    def LoadAndParse(self, configJson):        
        self.audit.AddMessage(au.Audit.INFO_START_AUDIT,'')
        with open(configJson) as f:
            content = f.read()
        self.parsed_json = json.loads(content)
        self.LoadAndParseDataFiles()
        self.ParseTransform()
        self.ParseAnalyze()
        return content

    def LoadAndParseDataFiles(self):
        files = []
        if not 'files' in self.parsed_json:
            self.audit.AddMessage(au.Audit.ERROR_CONFIG_DOES_NOT_CONTAIN_FILE_SECTION,'')
            return files

        count = len(self.parsed_json['files'])
        if count == 0:
            self.audit.AddMessage(au.Audit.ERROR_FILE_SECTION_EMPTY,'')
            return files

        for file in self.parsed_json['files']:
            newDataFile = df.DataFile(file, self.uploadFolder, self.audit)
            self.filesObj.append(newDataFile)
            newDataFile.ParseAndAudit()
        
        return files
    
    def ParseTransform(self):
        if not 'transform' in self.parsed_json:
            self.audit.AddMessage(au.Audit.ERROR_CONFIG_DOES_NOT_CONTAIN_TRANSFORM_SECTION,'')
        else:
            if 'merge' in self.parsed_json['transform']:
                if not 'from-filename' in self.parsed_json['transform']['merge']:
                    self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_SECTION_MERGE_MISSING_FROM_FILENAME,'')
                if not 'to-filename' in self.parsed_json['transform']['merge']:
                    self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_SECTION_MERGE_MISSING_TO_FILENAME,'')
                if not 'on-column' in self.parsed_json['transform']['merge']:
                    self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_SECTION_MERGE_MISSING_ON_COLUMN,'')

    def ParseAnalyze(self):
        if not 'analyze' in self.parsed_json:
            self.audit.AddMessage(au.Audit.ERROR_CONFIG_DOES_NOT_CONTAIN_ANALYZE_SECTION,'')

    def DataFiles(self):
        return self.filesObj

    def ValidateConfig(self):
        for file in self.filesObj:
            file.GetFilename()
            file.WorkingColumnHeaders()
            file.IsFileAvailable()

        return json.dumps(self.audit.messages, indent = 4, default=lambda o: o.__dict__)

    def GetAudit(self):
        return self.audit
        


    
