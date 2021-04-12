
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