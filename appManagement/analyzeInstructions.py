"""
This file contains classes which are initialized with the information from the
configuration JSON file. These objects decouple the JSON format with the
recommendation service code.

Classes
-------
    SparseStack
    VectorizeInstructions
    AnalyzeInstructions

Notes and Examples
------------------
"""

class SparseStack:
    identifier = None
    stackType = "hstack"
    stackFormat = "csr"
    vectorizedMatrixIds = []

    def __init__(self):
        self.identifier = None
        self.stackType = "hstack"
        self.stackFormat = "csr"
        self.vectorizedMatrixIds = []

class VectorizeInstructions:
    identifier = None
    vectorizerName = None
    stopWords = "english"
    column = None

    def __init__(self):
        self.identifier = None
        self.vectorizerName = None
        self.stopWords = "english"
        self.column = None

class AnalyzeInstructions:
    vectorizers = []
    sparseStack = []
    metrics = None

    def __init__(self):
        self.vectorizers = []
        self.sparseStack = []
        self.metrics = None


