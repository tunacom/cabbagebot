"""Simple functions to spread the joy of text based cabbage."""

import random


def spread_joy():
  """Spread the joy of cabbage.

  Returns:
     Joy.
  """
  return ' '.join(['cabbage'] * random.randint(1, 16))