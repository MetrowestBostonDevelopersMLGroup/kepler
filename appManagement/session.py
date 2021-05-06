import uuid
from appManagement import configMgr as cm
from engine import engine as eng
from dataclasses import dataclass

@dataclass
class Session:
  """
  Provides a place to store session information for the REST endpoints.
  Since REST is a stateless protocol, you need to be able to identify the session each call is associated with.
  Pass the session identifier to associate a parse/analyze operation with a recommendation operation.

  Parameters
  ----------
  sessions : configManager
      An instance of a class which is reponsible for managing, loading, parsing configuration data

  Attributes
  ----------

  Methods
  -------


  Raises
  ------
  ValueError

  Notes and Examples
  ------------------
    Each session has its own configuration manager object hierarchy which represents the configuration file properties.
    Each session also has its own recommendation engine object which contains the 'analyzed' data files and is central to recommendations.
  """

  configMgr: cm.ConfigMgr = None
  sessionId: str = None
  filename: str = None
  recEngine: eng.Engine = None

  def __init__(self, configManager: cm.ConfigMgr):
    self.configMgr = configManager

  # ----
  # Generates and returns new session identifier.
  # ----
  def getNewSID(self) -> str:
    self.sessionId = uuid.uuid4().hex
    return self.sessionId
  
  # ----
  # Stores the filename of the configuration associated with this session.
  # ----
  def setFilename(self, filename: str):
    self.filename = filename

  # ----
  # Retrieves the configuration manager associated with this session.
  # ----
  def getConfigMgr(self) -> cm.ConfigMgr:
    return self.configMgr

  # ----
  # Sets the recommendation engine associated with this session.
  # ----
  def setRecEngine(self, recEngine: eng.Engine):
    self.recEngine = recEngine

  # ----
  # Retrieves the recommendation engine associated with this session.
  # ----
  def getRecEngine(self) -> eng.Engine:
    return self.recEngine