"""This module define some user-defined exceptions"""

    
class OptionInputError(Exception):

    def __str__(self):
        return 'The option input format is wrong.'


class InvalidInputError(Exception):
    
    def __str__(self):
        return 'The input is invalid.'


class InputStationidFormatError(Exception):
    
    def __str__(self):
        return 'The input of station id has wrong format.'


class InputMonthFormatError(Exception):
    
    def __str__(self):
        return 'The input of month has wrong format.'


class InputDayFormatError(Exception):
    
    def __str__(self):
        return 'The input of day has wrong format.'


class InputStationidOutRange(Exception):
    
    def __str__(self):
        return 'The station ID does not exist.'


class InputDayOutRange(Exception):
    
    def __str__(self):
        return 'Input day is out of range.'


class InputMonthOutRange(Exception):
    
    def __str__(self):
        return 'Input month is out of range.'
