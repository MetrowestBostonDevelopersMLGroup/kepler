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

class WorkingColumn:

    header = None
    isJson = False
    isDelim = False
    isRegex = False
    extractElement = None
    separator = None
    itemCount = None
    expression = None

    def __init__(self):
        pass