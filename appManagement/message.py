from dataclasses import dataclass

class Message:
    """
    This file contains the properties that represent a message that is created as the result of
    loading, parsing and analyzing recommendation configuration and data files.

    Classes
    -------

    Notes and Examples
    ------------------
    """

    code: int = None
    message: str = None
    level: str = None   # Info, Warning, Error
    extra: str = None

    def __init__(self, code: int, message: str, level: str):
        self.code = code
        self.message = message
        self.level = level

