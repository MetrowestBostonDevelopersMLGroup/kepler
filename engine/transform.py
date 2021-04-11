from appManagement import dataFile as df

class Transform:

    def TransformDataFile(self, dataFile):
        dataFile.OrderWorkingFiles()
        dataFile.DropColumns()
        dataFile.WorkingColumnsConvertCompoundField()
        dataFile.RenameColumns()

    def MergeDataFiles(self, configMgr):        
        
        # merge the dataframe
        fromDataObj = configMgr.GetDataFileFromFilename(configMgr.transform.fromFilename)
        toDataObj = configMgr.GetDataFileFromFilename(configMgr.transform.toFilename)
        toDataObj.data = toDataObj.data.merge(fromDataObj.data, on=configMgr.transform.onColumn)

        #merge working columns
        toDataObj.workingColumns = toDataObj.workingColumns + fromDataObj.workingColumns
        
        # the combined working dataset to use for analysis purposes
        # TODO: return a datafile object even if a merge does not happen
        return toDataObj
