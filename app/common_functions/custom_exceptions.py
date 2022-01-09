"""This file containts custom exceptions used in this program.
"""


class UnknownException(Exception):
    """When you dont know reason of throwing exception.
    """
    
    def __init__(self, message):
        super.__init__(message)
    

class ValueTooLow(Exception):
    """ Raised when value is too low"""

    def __init__(self, message):
        super().__init__(message)


class ValueTooHigh(Exception):
    """ Raised when value is too high"""

    def __init__(self, message):
        super().__init__(message)


class IncorrectLimits(Exception):
    """Raised when lower limit is heigher than upper limit"""

    def __init__(self, message):
        super().__init__(message)


class IncorrectType(Exception):
    """Raised when argument has wrong type"""

    def __init__(self, message):
        super().__init__(message)


class IncorrectLen(Exception):
    """Raised when argument has wrong len"""

    def __init__(self, message):
        super().__init__(message)
