from appManagement import dataFile as df
from appManagement import configMgr as cf

class Transform:
    """
    Provides the engine with data transformation capability, specifically:
    - dropping columns
    - renaming columns
    - ordering columns
    - identifying the columns to 'work' with
    - parsing the row level data for 'complex' columms into a simpler format, such as:
        - JSON - columns that contain JSON formatted data
        - REGEX - apply regular expressions to extract information
        - DELIM - identify delimited data

    Parameters
    ----------
    configMgr : object
        An instance of a class which is reponsible for identifying the configuration 
        to use for recommendations
    dataFile: object
        An instance of the class resulting from the parsed data file JSON configuration

    Attributes
    ----------

    Methods
    -------
    TransformDataFile
    MergeDataFiles

    Raises
    ------

    Notes and Examples
    ------------------
    """

    def TransformDataFile(self, dataFile: df.DataFile):
        dataFile.OrderWorkingFiles()
        dataFile.DropColumns()
        dataFile.WorkingColumnsConvertCompoundField()
        dataFile.RenameColumns()

    def MergeDataFiles(self, configMgr: cf.ConfigMgr):        
        
        if configMgr.transform.fromFilename is None and configMgr.transform.toFilename is None:
            return configMgr.filesObj[0]

        # merge the dataframe
        fromDataObj = configMgr.GetDataFileFromFilename(configMgr.transform.fromFilename)
        toDataObj = configMgr.GetDataFileFromFilename(configMgr.transform.toFilename)
        toDataObj.data = toDataObj.data.merge(fromDataObj.data, on=configMgr.transform.onColumn)

        #merge working columns
        toDataObj.workingColumns = toDataObj.workingColumns + fromDataObj.workingColumns
        
        # the combined working dataset to use for analysis purposes
        # TODO: return a datafile object even if a merge does not happen
        return toDataObj
