"""Utility functions for rolling polyhedral cabbages."""

import enum
import random
import re

DICE_HELP_MESSAGE = (
    'PATHETIC HUMAN, YOU SEEM TO BE ATTEMPTING TO ROLL DICE INSTEAD OF '
    'CABBAGES. TRY ROLLING CABBAGES!\n'
    '(instead of rolling 1d20, try 1c20)')
INVALID_FORMULA_MESSAGE = (
    'PATHETIC HUMAN, YOUR CABBAGE FORMULA INVALID. TRY HARDER!')

DICE_REGEX = re.compile(r'd\d+')
TOKEN_REGEX = re.compile(r'(\d+|c|\+|-)')

MAX_CABBAGE_SIDES = 1000000000
MAX_FORMULA_LENGTH = 1000
MAX_POLYHEDRAL_CABBAGES = 100
MAX_TERMS = 5
ROLL_INDICATOR = 'c'
SIGN_MAPPINGS = {'+': 1, '-': -1}


@enum.unique
class ParseState(enum.Enum):
  sign_required = 0
  integer_or_roll_indicator = 1
  sign_or_roll_indicator = 2
  integer_required = 3


@enum.unique
class TermType(enum.Enum):
  constant = 0
  roll = 1


class Term(object):
  def __init__(self, term_type, sign, count=1, sides=0, value=0):
    self.term_type = term_type
    self.sign = sign
    self.cabbage_count = count
    self.sides = sides
    self.value = value


def roll_polyhedral_cabbage(formula):
  """Parse a polyhedral cabbage string.

  Expected to be in the form [A]cX[+BcY][+C]. Brackets denote optional terms.

  Uninformed, pathetic humans may try to roll polyhedral dice, but we do not
  support those. We should, however, let the humans know how uninformed and
  pathetic they are if they attempt to roll dice. We roll polyhedral cabbages
  in these parts.

  Args:
    formula: The unprocessed formula as a string.

   Returns:
     The roll result or error message.
  """
  if not formula:
    return 'NO CABBAGE ROLL SPECIFIED. TRY HARDER!'

  # TODO(tunacom): All of these messages should address the requesting user.
  if DICE_REGEX.search(formula):
    return DICE_HELP_MESSAGE

  if len(formula) > MAX_FORMULA_LENGTH:
    return 'CABBAGE FORMULA TOO LONG. DOES NOT COMPUTE!'

  # Ignore all whitespace in the formula.
  formula = re.sub(r'\s+', '', formula)

  # Split the formula into meaningful tokens (integers, "c", "+", and "-").
  tokens = [token for token in TOKEN_REGEX.split(formula) if token]

  # The first term is implied to be positive if unspecified.
  if tokens[0] != '-':
    tokens.insert(0, '+')

  # Add a sign to the end so that the last discord_token is finalized.
  tokens.append('+')

  terms = []
  state = ParseState.sign_required
  sign = 0
  left_value = 0

  for token in tokens:
    if len(terms) > MAX_TERMS:
      return 'TOO MANY TERMS IN CABBAGE FORMULA. DOES NOT COMPUTE!'

    if state == ParseState.sign_required:
      state = ParseState.integer_or_roll_indicator
      try:
        sign = SIGN_MAPPINGS[token]
      except KeyError:
        return INVALID_FORMULA_MESSAGE

    elif state == ParseState.integer_or_roll_indicator:
      # Check for the roll indicator first.
      if token == ROLL_INDICATOR:
        state = ParseState.integer_required
        left_value = 1  # Implied if no number is given.
        continue

      # In this case, we expect a number.
      state = ParseState.sign_or_roll_indicator
      try:
        left_value = int(token)
      except ValueError:
        return INVALID_FORMULA_MESSAGE

    elif state == ParseState.sign_or_roll_indicator:
      if token == ROLL_INDICATOR:
        state = ParseState.integer_required
        continue

      # Finalize the current term. In this case, it is a constant.
      term = Term(TermType.constant, sign, value=left_value)
      terms.append(term)

      state = ParseState.integer_or_roll_indicator
      try:
        sign = SIGN_MAPPINGS[token]
      except KeyError:
        return INVALID_FORMULA_MESSAGE

    elif state == ParseState.integer_required:
      state = ParseState.sign_required
      try:
        right_value = int(token)
      except ValueError:
        return INVALID_FORMULA_MESSAGE

      # Finalize the current term. In this case, it's a roll.
      term = Term(TermType.roll, sign, count=left_value, sides=right_value)
      terms.append(term)

  # TODO(tunacom): Move to another function, easy to make mistakes by shadowing
  # locals.
  total_rolls = 0
  result = 0
  math = ""
  for term in terms:
    sign_char = '+' if term.sign > 0 else '-'
    if term.term_type == TermType.constant:
      result += term.value * term.sign
      math += '{sign}{value}'.format(sign=sign_char, value=term.value)
    elif term.term_type == TermType.roll:
      # Limit the total number of rolls to avoid spam.
      total_rolls += term.cabbage_count
      if total_rolls > MAX_POLYHEDRAL_CABBAGES:
        return "I DON'T HAVE THAT MANY CABBAGES. SORRY!"
      if term.sides < 1:
        return "I DON'T EVEN KNOW WHAT A 0-SIDED CABBAGE IS!"
      if term.sides > MAX_CABBAGE_SIDES:
        return 'NO CABBAGE HAS THAT MANY SIDES. SORRY!'
      if term.cabbage_count < 1:
        return 'HOW TO ROLL NO CABBAGES? DOES NOT COMPUTE!'

      for _ in range(term.cabbage_count):
        roll = random.randint(1, term.sides)
        result += roll * term.sign
        math += '{sign}[{value}]'.format(sign=sign_char, value=roll)

  # Remove potential leading plus signs from the math for brevity.
  if math[0] == '+':
    math = math[1:]

  return '{result} ({math})'.format(result=result, math=math)
