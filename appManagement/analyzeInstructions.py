from typing import List
from dataclasses import dataclass

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

@dataclass
class SparseStack:
    identifier:str = None
    stackType:str = "hstack"
    stackFormat:str = "csr"
    vectorizedMatrixIds = []

    def __init__(self):
        self.identifier = None
        self.stackType = "hstack"
        self.stackFormat = "csr"
        self.vectorizedMatrixIds = []

@dataclass
class VectorizeInstructions:
    identifier:str = None
    vectorizerName:str = None
    stopWords:str = "english"
    column:str = None

    def __init__(self):
        self.identifier = None
        self.vectorizerName = None
        self.stopWords = "english"
        self.column = None

@dataclass
class AnalyzeInstructions:
    vectorizers = List[VectorizeInstructions]
    sparseStack = List[SparseStack]
    metrics = None

    def __init__(self):
        self.vectorizers = []
        self.sparseStack = []
        self.metrics = None


