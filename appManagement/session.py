import uuid

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
  recommend

  Raises
  ------
  ValueError

  Notes and Examples
  ------------------
    Each session has its own configuration manager object hierarchy which represents the configuration file properties.
    Each session also has its own recommendation engine object which contains the 'analyzed' data files and is central to recommendations.
  """

  configMgr = None
  sessionId = None
  filename = None
  recEngine = None

  def __init__(self, configManager):
    self.configMgr = configManager

  # ----
  # Generates and returns new session identifier.
  # ----
  def getNewSID(self):
    self.sessionId = uuid.uuid4().hex
    return self.sessionId
  
  # ----
  # Stores the filename of the configuration associated with this session.
  # ----
  def setFilename(self, filename):
    self.filename = filename

  # ----
  # Retrieves the configuration manager associated with this session.
  # ----
  def getConfigMgr(self):
    return self.configMgr

  # ----
  # Sets the recommendation engine associated with this session.
  # ----
  def setRecEngine(self, recEngine):
    self.recEngine = recEngine

  # ----
  # Retrieves the recommendation engine associated with this session.
  # ----
  def getRecEngine(self):
    return self.recEngine