from appManagement import dataFile as df

class Transform:

    def TransformDataFile(self, dataFile):
        dataFile.DropColumns()
        dataFile.RenameColumns()
        dataFile.CombineColumns()

    def MergeDataFiles(self, configMgr):        
        #data_movies = data_movies.merge(data_credits,on='movie_id')
        pass

        