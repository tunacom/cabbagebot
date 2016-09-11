"""Cabbage error helpers."""


class CabbageException(Exception):
  """Base class for cabbage-related exceptions."""
  def __init__(self, message):
    super().__init__(message)


class RecoverableCabbageException(CabbageException):
  """An easily recoverable cabbage-related exception."""
  def __init__(self, message):
    super().__init__(message)