"""This file containts custom exceptions used in this program.
"""


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
        super().__init__(self, message)


class IncorrectType(Exception):
    """Raised when argument has wrong type"""

    def __init__(self, message):
        super().__init__(self, message)


class IncorrectLen(Exception):
    """Raised when argument has wrong len"""

    def __init__(self, message):
        super().__init__(self, message)
