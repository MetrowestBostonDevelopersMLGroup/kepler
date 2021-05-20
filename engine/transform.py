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

    workingDataFile: df.DataFile = None

    # ---
    # Executes the steps to transform the datafile according to the configuration
    # ---
    def TransformDataFile(self, dataFile: df.DataFile):
        dataFile.OrderWorkingFiles()
        dataFile.DropColumns()
        dataFile.WorkingColumnsConvertCompoundField()
        dataFile.RenameColumns()

    # ---
    # Merges the data files together (if specified), otherwise does nothing and returns the DataFile object of the single file
    # ---
    def MergeDataFiles(self, configMgr: cf.ConfigMgr) -> df.DataFile:        
        
        if configMgr.transform.fromFilename is None and configMgr.transform.toFilename is None:
            self.workingDataFile = configMgr.filesObj[0]
            return configMgr.filesObj[0]

        # merge the dataframe
        fromDataObj = configMgr.GetDataFileFromFilename(configMgr.transform.fromFilename)
        toDataObj = configMgr.GetDataFileFromFilename(configMgr.transform.toFilename)
        toDataObj.data = toDataObj.data.merge(fromDataObj.data, on=configMgr.transform.onColumn)

        #merge working columns
        # the combined working dataset to use for analysis purposes
        toDataObj.workingColumns = toDataObj.workingColumns + fromDataObj.workingColumns
        
        self.workingDataFile = toDataObj
        return toDataObj

    # ---
    # Retrieves the transformed data which is now the 'working data file' object which represents the content on which recommendation analysis will occur
    # ---
    def GetWorkingDataFile(self) -> df.DataFile:   
        return self.workingDataFile