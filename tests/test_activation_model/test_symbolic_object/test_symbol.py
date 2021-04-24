import unittest

from neads.activation_model.symbolic_objects import *


class TestSymbol(unittest.TestCase):
    def setUp(self) -> None:
        self.symbol = Symbol()
        self.diff_symbol = Symbol()

        self.int_value = 0
        self.value = Value(self.int_value)

    def test_substitute_different_symbol(self):
        after_subs = self.symbol.substitute(self.diff_symbol, self.value)

        self.assertRaises(
            SymbolicObjectException,
            after_subs.get_value
        )
        self.assertIs(self.symbol, after_subs)

    def test_substitute_proper_symbol(self):
        after_subs = self.symbol.substitute(self.symbol, self.value)

        self.assertIsNot(self.symbol, after_subs)
        self.assertEqual(self.int_value, after_subs.get_value())

    def test_get_symbols(self):
        expected = [self.symbol]

        actual = self.symbol.get_symbols()

        self.assertCountEqual(expected, actual)

    def test_get_value(self):
        self.assertRaises(
            SymbolicObjectException,
            self.symbol.get_value
        )

    def test_eq_comparison_with_self(self):
        expected = True

        actual = self.symbol == self.symbol

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_different_symbol(self):
        expected = False

        actual = self.symbol == self.diff_symbol

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
