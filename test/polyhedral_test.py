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

    def test_long_formula(self):
        """Ensure that we don't attempt to parse very long formulae."""
        formula = '1' * 1001
        response = polyhedral.roll_polyhedral_cabbage(formula)
        self.assertIn('TOO LONG', response)

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

    def test_sides(self):
        """Ensure that we only roll polyhedral cabbages with valid sides."""
        response = polyhedral.roll_polyhedral_cabbage('1c0+1')
        self.assertIn('0-SIDED CABBAGE', response)

    def test_cabbage_count(self):
        """Ensure that we don't roll invalid numbers of cabbages."""
        response = polyhedral.roll_polyhedral_cabbage('101c6')
        self.assertIn("DON'T HAVE THAT MANY", response)

        response = polyhedral.roll_polyhedral_cabbage('100c6+c4')
        self.assertIn("DON'T HAVE THAT MANY", response)

        response = polyhedral.roll_polyhedral_cabbage('0c1')
        self.assertIn('HOW TO ROLL', response)

        response = polyhedral.roll_polyhedral_cabbage(
            '10c100000000000000000000')
        self.assertIn('NO CABBAGE HAS', response)

    @mock.patch('random.randint', return_value=17)  # The most random number.
    def test_roll(self, _):
        """Basic tests for several valid rolls.

    This must use a different return value than the stress tests.
    """
        response = polyhedral.roll_polyhedral_cabbage('c20')
        self.assertEquals(response, '17 ([17])')

        response = polyhedral.roll_polyhedral_cabbage('1c20')
        self.assertEquals(response, '17 ([17])')

        response = polyhedral.roll_polyhedral_cabbage('1c20-2')
        self.assertEquals(response, '15 ([17]-2)')

    @mock.patch('random.randint',
                return_value=2)  # Simulate Nigel as a halfing.
    def test_many_valid_rolls(self, _):
        """Regression/stress tests for many valid rolls."""
        formulae_and_results = {
            '1c2+1c3+1c4+1c5': '8 ([2]+[2]+[2]+[2])',
            '4c3': '8 ([2]+[2]+[2]+[2])',
            '1c2+1c3+1c4+2': '8 ([2]+[2]+[2]+2)',
            '1c2+1c3+1c4-2': '4 ([2]+[2]+[2]-2)',
            '-2+1c2+1c3+1c4': '4 (-2+[2]+[2]+[2])',
            '1c4+1+1c6': '5 ([2]+1+[2])',
            '100c4':
            '200 ([2]{repeated_math})'.format(repeated_math='+[2]' * 99)
        }

        for formula, result in formulae_and_results.items():
            response = polyhedral.roll_polyhedral_cabbage(formula)
            self.assertEquals(response, result)
