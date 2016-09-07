"""Unit tests for polyhedral cabbage fun."""

from unittest import mock
import unittest

from cabbage import polyhedral


class PolyhedralTest(unittest.TestCase):
  """Polyhedral cabbage tests."""

  def test_dice_error(self):
    """Ensure that silly humans are scolded for attempting to roll dice."""
    response = polyhedral.roll_polyhedral_cabbage('1d20')
    self.assertIn('TRY ROLLING CABBAGES', response)

  def test_formula_invalid(self):
    """Test that cabbagebot detects invalid formulae."""
    # Ensure that non-dice strings with d trigger an invalid formula message.
    response = polyhedral.roll_polyhedral_cabbage('donut')
    self.assertIn('TRY HARDER!', response)

    # Test actual invalid formulae.
    response = polyhedral.roll_polyhedral_cabbage('1c')
    self.assertIn('TRY HARDER!', response)

    # Ensure that the XcY format is properly enforced.
    response = polyhedral.roll_polyhedral_cabbage('c20+')
    self.assertIn('TRY HARDER!', response)

  @mock.patch('random.randint', return_value=7)  # The most random number.
  def test_roll(self, _):
    """Ensure that polyhedral cabbages can be rolled."""
    response = polyhedral.roll_polyhedral_cabbage('c20')
    self.assertEquals(response, '7 ([7])')

    response = polyhedral.roll_polyhedral_cabbage('1c20')
    self.assertEquals(response, '7 ([7])')

    response = polyhedral.roll_polyhedral_cabbage('1c20-2')
    self.assertEquals(response, '5 ([7]-2)')

  def test_sides(self):
    """Ensure that we only roll polyhedral cabbages with enough sides."""
    response = polyhedral.roll_polyhedral_cabbage('1c0+1')
    self.assertIn('0-SIDED CABBAGE', response)