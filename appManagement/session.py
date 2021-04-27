import uuid

class Session:

  configMgr = None
  sessionId = None
  filename = None
  recEngine = None

  def __init__(self, configManager):
    self.configMgr = configManager

  def getNewSID(self):
    self.sessionId = uuid.uuid4().hex
    return self.sessionId

  def setFilename(self, filename):
    self.filename = filename

  def getConfigMgr(self):
    return self.configMgr

  def setRecEngine(self, recEngine):
    self.recEngine = recEngine

  def getRecEngine(self):
    return self.recEngine