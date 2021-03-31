import uuid

class Session:

  def __init__(self, dataPrep, dataTransform, dataReady):
    self.dataPrep = dataPrep
    self.dataTransform = dataTransform
    self.dataReady = dataReady

  def setDataTransform(self, dataTransform):
    self.dataTransform = dataTransform

  def setDataReady(self, dataReady):
    self.dataReady = dataReady

  def getNewSID(self):
    return uuid.uuid4()
