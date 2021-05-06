from typing import List

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

class RecommendColumn:
    sourceColumn: str = None
    outputColumn: str = None

    def __init__(self):
        self.sourceColumn = None
        self.outputColumn = None

class Recommend:
    requestColumn: str = None
    responseCount: int = None
    responseColumns = List[RecommendColumn]

    def __init__(self):
        self.requestColumn = None
        self.responseCount = None
        self.responseColumns = []

