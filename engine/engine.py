from appManagement import audit as au
from appManagement import configMgr 
from engine import transform as xf
from engine import analyze as az
import pandas as pd

class Engine:

    configurationMgr = None
    transform = None
    analyze = None
    similarity = None
    finalDataObj = None

    def __init__(self, configurationManager):
        self.configurationMgr = configurationManager
        self.transform = xf.Transform()
        self.analyze = az.Analyze()

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

    def Recommendation(self, request):

        recommendation = self.analyze.Recommend(self.configurationMgr, self.finalDataObj.data, self.configurationMgr.recommend.requestColumn, request) #'Amavas') #'Aliens')

        return recommendation
