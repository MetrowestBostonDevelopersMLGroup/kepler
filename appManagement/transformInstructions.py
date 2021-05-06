from dataclasses import dataclass

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

@dataclass
class TransformInstructions:

    mergeDataFiles: bool = False
    fromFilename: str = None
    toFilename: str = None
    onColumn: str = None    

    def __init__(self):
        pass # nothing to do yet