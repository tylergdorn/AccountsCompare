"""
    Standard error handling for our program
"""
import logging
from typing import Callable

class FileLoadError(Exception):
    """Error when the file is loaded incorrectly"""
    pass

class ComparisonError(Exception):
    """Error when the files cannot be compared"""
    pass

def FileLoadDecorator(function: Callable):
    """This is probably bad practice. We condense down the error to a fileloaderror for easier handling on the frontend"""
    def wrapper(name):
        try:
            return function(name)
        except Exception:
            logging.exception("Serious error parsing file")
            raise FileLoadError
    return wrapper

def ComparisonDecorator(function: Callable):
    """Similar to FileLoadDecorator, but for the comparison"""
    def wrapper(first, second):
        try:
            return function(first, second)
        except Exception:
            logging.exception("Serious error comparing file")
            raise ComparisonError
    return wrapper