"""Helper script to run all cabbagebot unit tests."""

import os
import sys
import unittest


def main():
    """Run all tests."""
    pattern = '*_test.py'
    if len(sys.argv) > 1:
        pattern = sys.argv[1]

    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__), pattern=pattern)
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
