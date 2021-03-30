from appManagement import audit as au
from appManagement import configMgr 
from engine import transform as xf
from engine import analyze as az
import pandas as pd

class Engine:

    configurationMgr = None
    transform = None
    analyze = None

    def __init__(self, configurationManager):
        self.configurationMgr = configurationManager
        self.transform = xf.Transform()
        self.analyze = az.Analyze()

    def Execute(self):
        
        files = self.configurationMgr.DataFiles()
        for file in files:
            file.LoadData()
            self.transform.TransformDataFile(file)
        
        finalDataObj = self.transform.MergeDataFiles(self.configurationMgr)

        for file in files:
            file.CombineColumns()        

        similarity = self.analyze.VectorizeAndSimilarity(self.configurationMgr, finalDataObj)

        recommendation = self.analyze.Recommend(self.configurationMgr, finalDataObj.data, self.configurationMgr.recommend.requestColumn,'Aliens')

        return recommendation
