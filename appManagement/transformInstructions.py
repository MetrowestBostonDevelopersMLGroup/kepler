"""
This file contains classes which are initialized with the information from the
configuration JSON file. These objects decouple the JSON format with the
recommendation service code.

Classes
-------
    TransformInstructions

Notes and Examples
------------------
"""

class TransformInstructions:

    mergeDataFiles = False
    fromFilename = None
    toFilename = None
    onColumn = None    

    def __init__(self):
        pass # nothing to do yet