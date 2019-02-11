"""
    Standard error handling for our program
"""
class FileLoadError(Exception):
    """Error when the file is loaded incorrectly"""
    pass

class ComparisonError(Exception):
    """Error when the files cannot be compared"""
    pass

def FileLoadDecorator(function):
    """This is probably bad practice. We condense down the error to a fileloaderror for easier handling on the frontend"""
    def wrapper(name):
        try:
            return function(name)
        except Exception:
            raise FileLoadError
    return wrapper

def ComparisonDecorator(function):
    """Similar to FileLoadDecorator, but for the comparison"""
    def wrapper(name):
        try:
            return function(name)
        except Exception:
            raise ComparisonError
    return wrapper