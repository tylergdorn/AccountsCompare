"""
    Standard error handling for our program
"""
import logging
import functools
from typing import Callable

class FileLoadError(Exception):
    """Error when the file is loaded incorrectly"""
    pass

class ComparisonError(Exception):
    """Error when the files cannot be compared"""
    pass

def FileLoadDecorator(function: Callable): #type: ignore
    """This is probably bad practice. We condense down the error to a fileloaderror for easier handling on the frontend"""
    @functools.wraps(function)
    def wrapper(*args, **kwargs): #type: ignore
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Serious error parsing file: {e}")
            raise FileLoadError(e)
    return wrapper

def ComparisonDecorator(function: Callable): #type: ignore
    """Similar to FileLoadDecorator, but for the comparison"""
    @functools.wraps(function)
    def wrapper(*args, **kwargs): #type: ignore
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Serious error comparing file: {e}")
            raise ComparisonError(e)
    return wrapper