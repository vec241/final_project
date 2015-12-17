"""The errorhandler are the user defined errors for the program to
capture any possible errors."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

class Error(Exception):
   """Base class for other exceptions"""
   pass

class incorrectDate(Error):
   """Raised when the input value is too small"""
   pass

class incorrectDeviation(Error):
   """Raised when the input value is too large"""
   pass

class dateNotinFuture(Error):
   """Raised when the input value is too large"""
   pass
