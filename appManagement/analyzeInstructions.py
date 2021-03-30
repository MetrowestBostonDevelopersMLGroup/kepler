
class SparseStack:
    identifier = None
    stackType = "hstack"
    stackFormat = "csr"
    vectorizedMatrixIds = []


class VectorizeInstructions:
    identifier = None
    vectorizerName = None
    stopWords = "english"
    column = None


class AnalyzeInstructions:
    vectorizers = []
    sparseStack = []
    metrics = None


