import pandas as pd
import json
from flask import jsonify
from appManagement import dataFile as df
from appManagement import transformInstructions as ti
from appManagement import analyzeInstructions as vi
from appManagement import recommendInstructions as ri
from appManagement import audit as au

class ConfigMgr:
    
    parsed_json = None
    filesObj = []
    transform = None
    analyze = None
    recommend = None
    uploadFolder = None
    audit = None

    def __init__(self, uploadFolder):
        self.uploadFolder = uploadFolder
        self.audit = au.Audit()

    def LoadAndParse(self, configJson):       
        self.audit.ClearMessages() 
        self.audit.AddMessage(au.Audit.INFO_START_AUDIT,'')
        with open(configJson) as f:
            content = f.read()
        try:
            self.parsed_json = json.loads(content)
        except json.JSONDecodeError as ex:
            self.audit.AddMessage(au.Audit.ERROR_JSON_PARSE, ex.msg+' line:'+str(ex.lineno)+' col:'+str(ex.colno))
            return content, False

        self.LoadAndParseDataFiles()
        self.ParseTransform()
        self.ParseAnalyze()
        self.ParseRecommend()
        return content, True

    def Parse(self, content):       
        self.audit.ClearMessages() 
        self.audit.AddMessage(au.Audit.INFO_START_AUDIT,'')
        
        try:
            self.parsed_json = json.loads(content)
        except json.JSONDecodeError as ex:
            self.audit.AddMessage(au.Audit.ERROR_JSON_PARSE, ex.msg+' line:'+str(ex.lineno)+' col:'+str(ex.colno))
            return content, False

        self.LoadAndParseDataFiles()
        self.ParseTransform()
        self.ParseAnalyze()
        self.ParseRecommend()
        return content, True

    def GetAudit(self):
        return self.audit.messages

    def IsAuditError(self):
        audit = [x for x in self.GetAudit() if x.level == 'Error']
        if len(audit) > 0:
            return True
        return False

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
            newDataFile.ParseAndAudit()
            self.filesObj.append(newDataFile)
        
        return files
    
    def ParseTransform(self):
        if not 'transform' in self.parsed_json:
            self.audit.AddMessage(au.Audit.ERROR_CONFIG_DOES_NOT_CONTAIN_TRANSFORM_SECTION,'')
        else:
            self.transform = ti.TransformInstructions()
            if 'merge' in self.parsed_json['transform']:
                if not 'from-filename' in self.parsed_json['transform']['merge']:
                    self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_SECTION_MERGE_MISSING_FROM_FILENAME,'')
                else:
                    self.transform.fromFilename = self.parsed_json['transform']['merge']['from-filename']
                
                if not 'to-filename' in self.parsed_json['transform']['merge']:
                    self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_SECTION_MERGE_MISSING_TO_FILENAME,'')
                else:
                    self.transform.toFilename = self.parsed_json['transform']['merge']['to-filename']                    
                
                if not 'on-column' in self.parsed_json['transform']['merge']:
                    self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_SECTION_MERGE_MISSING_ON_COLUMN,'')
                else:
                    self.transform.onColumn = self.parsed_json['transform']['merge']['on-column']                    

    def ParseAnalyze(self):
        if not 'analyze' in self.parsed_json:
            self.audit.AddMessage(au.Audit.ERROR_CONFIG_DOES_NOT_CONTAIN_ANALYZE_SECTION,'')
        else:
            self.analyze = vi.AnalyzeInstructions()
            if not 'vectorizers' in self.parsed_json['analyze']:
                self.audit.AddMessage(au.Audit.ERROR_ANALYZE_SECTION_MISSING_VECTORIZERS,'')
            else:
                for vect in self.parsed_json['analyze']['vectorizers']:
                    vectorize = vi.VectorizeInstructions()

                    if not 'id' in vect:
                        self.audit.AddMessage(au.Audit.ERROR_VECTORIZER_SECTION_MISSING_ID,'')
                    else:
                        vectorize.identifier = vect['id']                           

                    if not 'vectorizer' in vect:
                        self.audit.AddMessage(au.Audit.ERROR_VECTORIZER_SECTION_MISSING_VECTORIZER,'')
                    else:
                        vectorize.vectorizerName = vect['vectorizer']                           

                    if not 'stop-words' in vect:
                        self.audit.AddMessage(au.Audit.WARNING_VECTORIZER_SECTION_MISSING_STOPWORDS,'')
                    else:
                        vectorize.stopWords = vect['stop-words']                           

                    if not 'column' in vect:
                        self.audit.AddMessage(au.Audit.ERROR_VECTORIZER_SECTION_MISSING_COLUMN,'')
                    else:
                        vectorize.column = vect['column']                           

                    self.analyze.vectorizers.append(vectorize)

            if not 'sparse-stack' in self.parsed_json['analyze']:
                self.audit.AddMessage(au.Audit.ERROR_ANALYZE_SECTION_NOT_CONTAIN_SPARSE_STACK,'')
            else:      
                for sparse in self.parsed_json['analyze']['sparse-stack']:      
                    stack = vi.SparseStack()

                    if not 'id' in sparse:
                        self.audit.AddMessage(au.Audit.ERROR_SPARSE_STACK_SECTION_MISSING_ID,'')
                    else:
                        stack.identifier = sparse['id']                           

                    if not 'stack-type' in sparse:
                        self.audit.AddMessage(au.Audit.ERROR_SPARSE_STACK_SECTION_MISSING_STACK_TYPE, stack.identifier)
                    else:
                        stack.stackType = sparse['stack-type']                           

                    if not 'format' in sparse:
                        self.audit.AddMessage(au.Audit.ERROR_SPARSE_STACK_SECTION_MISSING_STACK_FORMAT,stack.identifier)
                    else:
                        stack.stackFormat = sparse['format']                           

                    if not 'vectorized-matrix-ids' in sparse:
                        self.audit.AddMessage(au.Audit.ERROR_SPARSE_STACK_SECTION_MISSING_VECT_MATRIX_IDS,stack.identifier)
                    else:
                        for vectmatid in sparse['vectorized-matrix-ids']:      
                            stack.vectorizedMatrixIds.append(vectmatid)                       

                    self.analyze.sparseStack.append(stack)

            if not 'metrics' in self.parsed_json['analyze']:
                self.audit.AddMessage(au.Audit.ERROR_ANALYZE_SECTION_NOT_CONTAIN_METRICS,'')
            else:      
                if not 'similarity' in self.parsed_json['analyze']['metrics']:   
                    self.audit.AddMessage(au.Audit.ERROR_ANALYZE_METRICS_MISSING_SIMILARITY,'')
                else:
                    stack.similarity = self.parsed_json['analyze']['metrics']['similarity']                 

    def ParseRecommend(self):
        if not 'recommend' in self.parsed_json:
            self.audit.AddMessage(au.Audit.ERROR_CONFIG_DOES_NOT_CONTAIN_RECOMMEND_SECTION,'')
        else:
            self.recommend = ri.Recommend()
            if not 'request-column' in self.parsed_json['recommend']:
                self.audit.AddMessage(au.Audit.ERROR_RECOMMEND_SECTION_MISSING_REQUEST_COLUMN_ATTRIBUTE,'')
            else:
                self.recommend.requestColumn =  self.parsed_json['recommend']['request-column']

            if not 'response-count' in self.parsed_json['recommend']:
                self.audit.AddMessage(au.Audit.ERROR_RECOMMEND_SECTION_MISSING_RESPONSE_COUNT_ATTRIBUTE,'')
            else:
                self.recommend.responseCount =  self.parsed_json['recommend']['response-count']

            if not 'response-columns' in self.parsed_json['recommend']:
                self.audit.AddMessage(au.Audit.ERROR_RECOMMEND_SECTION_MISSING_RESPONSE_COLUMNS,'')
            else:
                for col in self.parsed_json['recommend']['response-columns']:
                    column = ri.RecommendColumn()

                    if not 'source' in col:
                        self.audit.AddMessage(au.Audit.ERROR_RECOMMEND_SECTION_MISSING_SOURCE_COLUMN,'')
                    else:
                        column.sourceColumn = col['source']      

                    if not 'output' in col:
                        self.audit.AddMessage(au.Audit.ERROR_RECOMMEND_SECTION_MISSING_OUTPUT_COLUMN,'')
                    else:
                        column.outputColumn = col['output'] 

                    self.recommend.responseColumns.append(column)

    def DataFiles(self):
        return self.filesObj

    def ValidateConfig(self):
        for file in self.filesObj:
            file.GetFilename()
            file.WorkingColumnHeaders()
            file.IsFileAvailable()

        return json.dumps(self.audit.messages, indent = 4, default=lambda o: o.__dict__)
       
    def GetDataFileFromFilename(self, filename):
        files = [item for item in self.filesObj if item.GetFilename() == filename]
        return files[0]

    def GetRequestColumnName(self):
        if self.recommend is not None:
            return self.recommend.requestColumn 
        return ''

    
