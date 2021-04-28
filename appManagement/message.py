
class Message:
    """
    This file contains the properties that represent a message that is created as the result of
    loading, parsing and analyzing recommendation configuration and data files.

    Classes
    -------

    Notes and Examples
    ------------------
    """

    code = None
    message = None
    level = None   # Info, Warning, Error
    extra = None

    def __init__(self, code, message, level):
        self.code = code
        self.message = message
        self.level = level

