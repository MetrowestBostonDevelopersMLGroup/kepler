from dataclasses import dataclass

"""
This file contains classes which are initialized with the information from the
configuration JSON file. These objects decouple the JSON format with the
recommendation service code.

Classes
-------
    WorkingColumn

Notes and Examples
------------------
"""

@dataclass
class WorkingColumn:

    header: str = None
    isJson: bool = False
    isDelim: bool = False
    isRegex: bool = False
    extractElement: str = None
    separator: str = None
    itemCount: int = None
    expression: str = None

    def __init__(self):
        pass