from appManagement import audit as au
from appManagement import configMgr 
from engine import transform as xf
from engine import analyze as az
import pandas as pd

class Engine:
    """
    Given a configuration manager instance, this object will organize:
    - the loading of the datafiles
    - the parsing of the datafiles into objects
    - coordinates the ETL of the data
    - configures the recommendation engine specifics and analyzes the data
    - provides a method to produce recommendations

    Parameters
    ----------
    configurationManager : object
        An instance of a class which is reponsible for identifying the configuration 
        to use for recommendations

    Attributes
    ----------

    Methods
    -------
    recommend

    Raises
    ------
    ValueError
        If the categories do not validate.

    Notes and Examples
    ------------------
    """

    configurationMgr = None
    transform = None
    analyze = None
    similarity = None
    finalDataObj = None

    def __init__(self, configurationManager):
        self.configurationMgr = configurationManager
        self.transform = xf.Transform()
        self.analyze = az.Analyze()
        self.similarity = None
        self.finalDataObj = None

    # ---
    # Performs the loading, parsing and processing of the data files making the system available to issue recommendations.
    # ---
    def Execute(self):
        
        files = self.configurationMgr.DataFiles()
        for file in files:
            file.LoadData()
            self.transform.TransformDataFile(file)
        
        self.finalDataObj = self.transform.MergeDataFiles(self.configurationMgr)

        for file in files:
            file.CombineColumns()        

        self.similarity = self.analyze.VectorizeAndSimilarity(self.configurationMgr, self.finalDataObj)

        return self.similarity

    # ---
    # Accepts a request and provides a recommendation, or empty set.
    # ---
    def Recommendation(self, request):

        recommendation = self.analyze.Recommend(self.configurationMgr, self.finalDataObj.data, self.configurationMgr.recommend.requestColumn, request) #'Amavas') #'Aliens')

        return recommendation
