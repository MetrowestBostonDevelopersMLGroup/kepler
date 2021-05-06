import json
import os
import re
import pandas as pd
from appManagement import message as mes
from appManagement import audit as au
from appManagement import workingColumn as wc
from appManagement import combineColumn as cc
from typing import List
from dataclasses import dataclass

class DataFile:
    jsonObj = None          # result of the json.loads operation
    uploadFolder: str = None     # the upload file path
    audit: au.Audit              # the audit instance
    data = None             # Dataframe from pandas.read_csv
    workingColumns = List[wc.WorkingColumn]     # collection of WorkingColumn objects
    combineColumns = List[cc.CombineColumn]     # collection of CombineColumn objects
    na_filter: bool = True
    error_bad_lines: bool = False

    def __init__(self, dataObject, uploadFolder: str, audit: au.Audit):
        self.jsonObj = dataObject
        self.uploadFolder = uploadFolder
        self.audit = audit
        self.workingColumns = []
        self.combineColumns = []
        self.data = None        
        self.na_filter = True
        self.error_bad_lines = False

    # ----
    # Parses a specific file configuration
    # ----
    def ParseAndAudit(self):
        hasFilename = True
        if not 'filename' in self.jsonObj:
            self.audit.AddMessage(au.Audit.ERROR_FILE_SECTION_DOES_NOT_CONTAIN_FILENAME,'')
            hasFilename = False
        if not 'na-filter' in self.jsonObj:
            self.audit.AddMessage(au.Audit.WARNING_FILE_SECTION_DOES_NOT_CONTAIN_NA_FILTER,'')
        else:
            self.na_filter = self.to_bool(self.jsonObj['na-filter'])

        if not 'error-bad-lines' in self.jsonObj:
            self.audit.AddMessage(au.Audit.WARNING_FILE_SECTION_DOES_NOT_CONTAIN_ERROR_BAD_LINES,'') 
        else:
            self.error_bad_lines = self.to_bool(self.jsonObj['error-bad-lines'])

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

    # ----
    # String to bool
    # ----
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

    # ----
    # TODO
    # ----
    def Validate(self):
        return 'ok'    

    # ----
    # Determines if the 'physical' file associated with the datafile instance has been uploaded and is available to load.
    # ----
    def IsFileAvailable(self):
        avail = os.path.isfile(self.uploadFolder+'/'+self.GetFilename())
        if not avail:
            self.audit.AddMessage(au.Audit.ERROR_DATAFILE_NOT_UPLOADED, self.GetFilename())
        else:
            pass
        return avail

    # ----
    # Loads the associated data file.
    # ----
    def LoadData(self):
        self.data = pd.read_csv(self.uploadFolder+'/'+self.GetFilename(), na_filter=self.GetNAFilter(), error_bad_lines = self.GetErrorBadLines())
    
    # ----
    # Returns the filename from the JSON object
    # ----
    def GetFilename(self):
        return self.jsonObj['filename']
    
    # ----
    # Returns the NA filter for the file. see pandas.read_csv
    # ----
    def GetNAFilter(self):
        return self.na_filter 

    # ----
    # Returns the error_bad_lines for the file. see pandas.read_csv
    # ----
    def GetErrorBadLines(self):
        return self.error_bad_lines 

    # ----
    # Returns a collection of the column names for the working columns
    # ----       
    def WorkingColumnHeaders(self): 
        titles = []
        for work in self.jsonObj['workingColumns']:
            titles.append(work['header'])
        return titles

    # ----
    # Processes the contents of 'complex' columns into something that is simpler.
    # Implements the code to convert:
    #   - JSON columns
    #   - Delimited columns
    #   - Regex extraction
    # ----
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

    # ----
    # Drops the columns specified in the configuration for this file.
    # ----   
    def DropColumns(self):        
        try:
            if 'drop' in self.jsonObj:
                self.data = self.data.drop(columns=self.jsonObj['drop'])
        except Exception as ex:
            self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_DROP_COLUMN_EXCEPTION, ex)        

    # ----
    # Renames the columns specified in the configuration for this file.
    # ----   
    def RenameColumns(self):
        try:
            if 'rename' in self.jsonObj:
                for renamed in self.jsonObj['rename']:
                    self.data = self.data.rename(columns=renamed)
        except Exception as ex:
            self.audit.AddMessage(au.Audit.ERROR_TRANSFORM_RENAME_COLUMN_EXCEPTION, ex)                

    # ----
    # Combines the columns specified in the configuration for this file.
    # ----   
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

        return [] 

    # ----
    # Lambda performing the JSON column conversion.
    #   - jsonData      - the cell data to parse
    #   - returnCount   - the number of matches to return
    #   - attributeName - the attibute to match on
    # ----   
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

    # ----
    # Lambda performing the delimited column conversion.
    #   - cellata       - the cell data to parse
    #   - returnCount   - the number of matches to return
    #   - separator     - the character to separate by
    # ----   
    def get_list_delim(self, cellData, returnCount, separator):
        try:
            as_list = cellData.split(separator)
            as_list = as_list[:returnCount]
            return as_list
        except Exception:
            return []
        return []

    # ----
    # Lambda performing the Regex column conversion.
    #   - cellData      - the cell data to parse
    #   - returnCount   - the number of matches to return
    #   - expression    - the regex to apply
    # ----   
    def get_list_regex(self, cellData, returnCount, expression):  # r"\(u'(.*?)',\)"
        try:
            as_list = re.findall(expression, cellData) 
            as_list = as_list[:returnCount]
            return as_list
        except Exception:
            return []
        return []

    # ----
    # Orders the columns in working-column order
    # ----   
    def OrderWorkingFiles(self):
        self.data = self.data[self.WorkingColumnHeaders()]        