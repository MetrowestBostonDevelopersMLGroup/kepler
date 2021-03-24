from appManagement import audit as au
from appManagement import configMgr 
from engine import transform as xf
import pandas as pd

class Engine:

    configurationMgr = None
    transform = None

    def __init__(self, configurationManager):
        self.configurationMgr = configurationManager
        self.transform = xf.Transform()

    def Execute(self):
        files = self.configurationMgr.DataFiles()
        for file in files:
            file.LoadData()
            self.transform.TransformDataFile(file)
        self.transform.MergeDataFiles(self.configurationMgr)
