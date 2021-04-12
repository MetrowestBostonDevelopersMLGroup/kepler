import json
import os
import re
import pandas as pd
from appManagement import message as mes
from appManagement import audit as au
from appManagement import workingColumn as wc
from appManagement import combineColumn as cc

class DataFile:
    jsonObj = None
    uploadFolder = None
    audit = []
    data = None
    workingColumns = []
    combineColumns = []

    def __init__(self, dataObject, uploadFolder, audit):
        self.jsonObj = dataObject
        self.uploadFolder = uploadFolder
        self.audit = audit
        self.workingColumns = []
        self.combineColumns = []
        self.data = None        

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
                workObj = wc.WorkingColumn()
                if not 'header' in work:
                    self.audit.AddMessage(au.Audit.ERROR_WORKING_COLUMN_MISSING_HEADER_ATTRIBUTE,'')
                else:
                    workObj.header = work['header']  
                try:
                    if 'is-json' in work:
                        workObj.isJson = self.to_bool(work['is-json'])

                        if workObj.isJson:
                            if not 'extract-element' in work:
                                self.audit.AddMessage(au.Audit.ERROR_WORKING_COLUMN_MISSING_EXTRACT_ELEMENT_ATTRIBUTE,workObj.header)
                            else:
                                workObj.extractElement = work['extract-element']  

                            if not 'item-count' in work:
                                self.audit.AddMessage(au.Audit.WARNING_WORKING_COLUMN_MISSING_ITEM_COUNT_ATTRIBUTE,workObj.header)
                            else:
                                workObj.itemCount = work['item-count']                                  

                except Exception as ex:
                    self.audit.AddMessage(au.Audit.ERROR_WORKING_COLUMN_IS_JSON_ATTRIBUTE, ex)

                try:
                    if 'is-delim' in work:
                        workObj.isDelim = self.to_bool(work['is-delim'])

                        if workObj.isDelim:
                            if not 'separator' in work:
                                self.audit.AddMessage(au.Audit.ERROR_WORKING_COLUMN_MISSING_SEPARATOR_ATTRIBUTE,workObj.header)
                            else:
                                workObj.separator = work['separator']  

                            if not 'item-count' in work:
                                self.audit.AddMessage(au.Audit.WARNING_WORKING_COLUMN_MISSING_ITEM_COUNT_ATTRIBUTE,workObj.header)
                            else:
                                workObj.itemCount = work['item-count']                                  
                except Exception as ex:
                    self.audit.AddMessage(au.Audit.ERROR_WORKING_COLUMN_IS_DELIM_ATTRIBUTE, ex)

                try:
                    if 'is-regex' in work:
                        workObj.isRegex = self.to_bool(work['is-regex'])

                        if workObj.isRegex:
                            if not 'expression' in work:
                                self.audit.AddMessage(au.Audit.ERROR_WORKING_COLUMN_MISSING_EXPRESSION_ATTRIBUTE,workObj.header)
                            else:
                                workObj.expression = work['expression']  

                            if not 'item-count' in work:
                                self.audit.AddMessage(au.Audit.WARNING_WORKING_COLUMN_MISSING_ITEM_COUNT_ATTRIBUTE,workObj.header)
                            else:
                                workObj.itemCount = work['item-count']       
                except Exception as ex:
                    self.audit.AddMessage(au.Audit.ERROR_WORKING_COLUMN_IS_REGEX_ATTRIBUTE, ex)

                self.workingColumns.append(workObj)
        
        if 'combineColumns' in self.jsonObj:
            for combine in self.jsonObj['combineColumns']:
                combineObj = cc.CombineColumn()
                if not 'combine-header' in combine:
                    self.audit.AddMessage(au.Audit.ERROR_COMBINE_COLUMN_MISSING_COMBINE_HEADER_ATTRIBUTE,'')
                else:
                    combineObj.combineHeader = combine['combine-header']  

                if not 'column1' in combine:
                    self.audit.AddMessage(au.Audit.ERROR_COMBINE_COLUMN_MISSING_COLUMN1_ATTRIBUTE,'')
                else:
                    combineObj.column1 = combine['column1']  

                if not 'column2' in combine:
                    self.audit.AddMessage(au.Audit.ERROR_COMBINE_COLUMN_MISSING_COLUMN2_ATTRIBUTE,'')
                else:
                    combineObj.column2 = combine['column2']  

                if not 'item-count' in combine:
                    self.audit.AddMessage(au.Audit.WARNING_COMBINE_COLUMN_MISSING_ITEM_COUNT_ATTRIBUTE,'')
                else:
                    combineObj.itemCount = combine['item-count']  

                if not 'drop-source-columns' in combine:
                    self.audit.AddMessage(au.Audit.WARNING_COMBINE_COLUMN_MISSING_DROP_SOURCE_COLUMNS_ATTRIBUTE,'')
                else:
                    combineObj.dropSourceColumns = combine['drop-source-columns']  

                if combineObj.combineHeader is not None:
                    self.combineColumns.append(combineObj)

        return 'ok'

    def to_bool(self, value):
        valid = {'true': True, 't': True, '1': True,
                'false': False, 'f': False, '0': False,
                }   

        if isinstance(value, bool):
            return value

        if not isinstance(value, str):
            raise ValueError('invalid literal for boolean. Not a string.')

        lower_value = value.lower()
        if lower_value in valid:
            return valid[lower_value]
        else:
            raise ValueError('invalid literal for boolean: "%s"' % value)


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

    def WorkingColumnsConvertCompoundField(self): 
        for workCol in self.workingColumns:
            if workCol.isJson:
                if workCol.extractElement is not None and workCol.itemCount is not None:
                    self.data[workCol.header] = self.data[workCol.header].apply(lambda x: self.get_list_json(x, workCol.itemCount,workCol.extractElement))
                    continue
            if workCol.isDelim:
                if workCol.separator is not None and workCol.itemCount is not None:
                    self.data[workCol.header] = self.data[workCol.header].apply(lambda x: self.get_list_delim(x, workCol.itemCount,workCol.separator))
                    continue
            if workCol.isRegex:
                if workCol.expression is not None and workCol.itemCount is not None:
                    self.data[workCol.header] = self.data[workCol.header].apply(lambda x: self.get_list_regex(x, workCol.itemCount,workCol.expression))
                    continue                

    def DropColumns(self):        
        try:
            if 'drop' in self.jsonObj:
                self.data = self.data.drop(columns=self.jsonObj['drop'])
        except Exception as ex:
            self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_DROP_COLUMN_EXCEPTION, ex)        

    def RenameColumns(self):
        try:
            if 'rename' in self.jsonObj:
                for renamed in self.jsonObj['rename']:
                    self.data = self.data.rename(columns=renamed)
        except Exception as ex:
            self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_RENAME_COLUMN_EXCEPTION, ex)                

    def CombineColumns(self):       
        for combine in self.combineColumns:
            col1 = None
            col2 = None

            if combine.column1 is None:
                pass

            #find column1            
            for col in self.workingColumns:
                if col.header == combine.column1:
                    col1 = col
                    break
            else:
                self.audit.AddMessage(au.Audit.ERROR_COMBINE_COLUMN1_NOT_WORKING_COLUMN, combine.column1)                               

            #find column2
            for col in self.workingColumns:
                if col.header == combine.column2:
                    col2 = col
                    break
            else:
                self.audit.AddMessage(au.Audit.ERROR_COMBINE_COLUMN2_NOT_WORKING_COLUMN, combine.column2)               
            
            self.data[combine.combineHeader] = self.data[[col1.header,col2.header]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)

        return [] # actually perform the combine operation

    def get_list_json(self, jsonData, returnCount, attributeName):       
        try:
            if isinstance(jsonData, str):        
                parsed_json = json.loads(jsonData)
                parsed_json = parsed_json[:returnCount]
                result = []
                for item in parsed_json:
                    result.append(item[attributeName])
                return result
        except Exception:
            return []
        return []

    def get_list_delim(self, cellData, returnCount, separator):
        try:
            as_list = cellData.split(separator)
            as_list = as_list[:returnCount]
            return as_list
        except Exception:
            return []
        return []

    def get_list_regex(self, cellData, returnCount, expression):  # r"\(u'(.*?)',\)"
        try:
            as_list = re.findall(expression, cellData) 
            as_list = as_list[:returnCount]
            return as_list
        except Exception:
            return []
        return []

    def OrderWorkingFiles(self):
        # do similar to: data_credits = data_credits[['movie_id','title','cast','crew']]
        self.data = self.data[self.WorkingColumnHeaders()]        