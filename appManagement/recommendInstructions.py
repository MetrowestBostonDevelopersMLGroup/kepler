"""
This file contains classes which are initialized with the information from the
configuration JSON file. These objects decouple the JSON format with the
recommendation service code.

Classes
-------
    Recommend
    RecommendColumn

Notes and Examples
------------------
"""

class Recommend:
    requestColumn = None
    responseCount = None
    responseColumns = []

    def __init__(self):
        self.requestColumn = None
        self.responseCount = None
        self.responseColumns = []

class RecommendColumn:
    sourceColumn = None
    outputColumn = None

    def __init__(self):
        self.sourceColumn = None
        self.outputColumn = None