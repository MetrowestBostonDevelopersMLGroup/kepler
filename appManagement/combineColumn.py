from dataclasses import dataclass

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

@dataclass
class CombineColumn:

    combineHeader: str = None
    column1: str = None
    column2: str = None
    itemCount: int = None
    dropSourceColumns: bool = True
