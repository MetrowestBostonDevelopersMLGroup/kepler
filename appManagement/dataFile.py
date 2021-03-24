import json
import os
import pandas as pd
from appManagement import message as mes
from appManagement import audit as au

class DataFile:
    jsonObj = None
    uploadFolder = None
    audit = []
    data = None

    def __init__(self, dataObject, uploadFolder, audit):
            self.jsonObj = dataObject
            self.uploadFolder = uploadFolder
            self.audit = audit

    def ParseAndAudit(self):
        hasFilename = True
        if not 'filename' in self.jsonObj:
            self.audit.AddMessage(au.Audit.ERROR_FILE_SECTION_DOES_NOT_CONTAIN_FILENAME,'')
            hasFilename = False
        if not 'na-filter' in self.jsonObj:
            self.audit.AddMessage(au.Audit.WARNING_FILE_SECTION_DOES_NOT_CONTAIN_NA_FILTER,'')
        if hasFilename:
            self.IsFileAvailable()
        
        if not 'drop' in self.jsonObj:
            self.audit.AddMessage(au.Audit.WARNING_FILE_SECTION_DOES_NOT_CONTAIN_COLUMNS_TO_DROP,'')
        if not 'rename' in self.jsonObj:
            self.audit.AddMessage(au.Audit.WARNING_FILE_SECTION_DOES_NOT_CONTAIN_COLUMNS_TO_RENAME,'')

        hasWorkingColumns = True
        if not 'workingColumns' in self.jsonObj:
            self.audit.AddMessage(au.Audit.ERROR_FILE_SECTION_DOES_NOT_CONTAIN_WORKING_COLUMNS,'')
            hasWorkingColumns = False

        if hasWorkingColumns:
            for work in self.jsonObj['workingColumns']:
                print(work)
        
        return 'ok'

    def Validate(self):
        return 'ok'    

    def IsFileAvailable(self):
        avail = os.path.isfile(self.uploadFolder+'/'+self.GetFilename())
        if not avail:
            self.audit.AddMessage(au.Audit.ERROR_DATAFILE_NOT_UPLOADED, self.GetFilename())
        else:
            pass
        return avail

    def LoadData(self):
        self.data = pd.read_csv(self.uploadFolder+'/'+self.GetFilename(), na_filter=self.GetNAFilter())

    def GetFilename(self):
        return self.jsonObj['filename']

    def GetNAFilter(self):
        return self.jsonObj['na-filter']

    def Table(self):
        return None
        
    def WorkingColumnHeaders(self): 
        titles = []
        for work in self.jsonObj['workingColumns']:
            titles.append(work['header'])
        return titles

    def DropColumns(self):
        try:
            if 'drop' in self.jsonObj:
                self.data = self.data.drop(columns=self.jsonObj['drop'])
        except Exception as ex:
            self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_DROP_COLUMN_EXCEPTION, ex)        

    def RenameColumns(self):
        try:
            if 'rename' in self.jsonObj:
                self.data = self.data.drop(columns=self.jsonObj['rename'])
        except Exception as ex:
            self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_RENAME_COLUMN_EXCEPTION, ex)                

    def CombineColumns(self):
        return []