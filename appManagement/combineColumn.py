"""
This file contains classes which are initialized with the information from the
configuration JSON file. These objects decouple the JSON format with the
recommendation service code.

Classes
-------
    CombineColumn

Notes and Examples
------------------
"""

class CombineColumn:

    combineHeader = None
    column1 = None
    column2 = None
    itemCount = None
    dropSourceColumns = True
