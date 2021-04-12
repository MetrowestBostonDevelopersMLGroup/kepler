
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


