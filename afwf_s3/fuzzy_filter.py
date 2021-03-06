# -*- coding: utf-8 -*-

"""
Fuzzy search support
"""

from typing import List, Dict, Any
from fuzzywuzzy import process


class FuzzyObjectSearch(object):
    """
    A simple wrapper around fuzzywuzzy search.

    The actual data stored in ``mapper``, the search scope is the key of the
    actual data. You can use key to access the actual data.

    :type keys: list[str]
    :type mapper: typing.Dict[str, typing.Any]
    """

    def __init__(self, keys: List[str], mapper: Dict[str, Any]):
        self.keys = keys
        self.mapper = mapper

    def match(self, query, limit=20) -> List[Any]:
        return [
            self.mapper[key]
            for key, score in process.extract(query, self.keys, limit=limit)
        ]
