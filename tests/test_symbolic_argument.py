import unittest
import itertools

from neads.symbolic_argument import *


class TestSimpleArgument(unittest.TestCase):

    def compare_iterables_content(self, expected_iterable, actual_iterable):
        """Test content of iterables while abstracting their actual type."""
        exp_expanded = list(expected_iterable)
        act_expanded = list(actual_iterable)
        self.assertEqual(exp_expanded, act_expanded)

    def setUp(self) -> None:
        self.INT_VALUE = 100
        self.symbol_a = Symbol('a')
        self.symbol_b = Symbol('b')
        self.value = Value(self.INT_VALUE)
        self.simple_symb_a = SimpleArgument(self.symbol_a)
        self.simple_val = SimpleArgument(self.value)

    def test_get_actual_argument_value_with_symbol(self):
        self.assertRaises(
            SymbolicArgumentException,
            self.simple_symb_a.get_actual_argument_value
        )

    def test_get_actual_argument_value_with_value(self):
        actual_value = self.simple_val.get_actual_argument_value()
        self.assertEqual(self.INT_VALUE, actual_value)

    def test_get_symbols_with_symbol(self):
        expected_iterable = [self.symbol_a]
        actual_iterable = self.simple_symb_a.get_symbols()
        self.compare_iterables_content(expected_iterable, actual_iterable)

    def test_get_symbols_with_value(self):
        expected_iterable = []
        actual_iterable = self.simple_val.get_symbols()
        self.compare_iterables_content(expected_iterable, actual_iterable)

    def test_substitute_value_incorrect_symbol(self):
        not_symbol = 'this string is not a symbol'
        self.assertRaises(
            TypeError,
            self.simple_symb_a.substitute_value,
            not_symbol,
            self.value
        )

    def test_substitute_value_incorrect_value(self):
        not_value = 'this string is not a value'
        self.assertRaises(
            TypeError,
            self.simple_symb_a.substitute_value,
            self.symbol_a,
            not_value
        )

    def test_substitute_value_to_value_arg(self):
        ret_val = self.simple_val.substitute_value(self.symbol_a, self.value)

        self.assertEqual(False, ret_val)
        # Test that content of simple_val has not changed
        self.assertEqual(self.INT_VALUE,
                         self.simple_val.get_actual_argument_value())

    def test_substitute_value_to_symbol_arg_with_different_symbol(self):
        ret_val = self.simple_symb_a.substitute_value(self.symbol_b, self.value)

        self.assertEqual(False, ret_val)
        # Test that content of simple_symb_a has not changed
        expected = [self.symbol_a]
        self.compare_iterables_content(expected,
                                       self.simple_symb_a.get_symbols())

    def test_substitute_value_nominal_case(self):
        ret_val = self.simple_symb_a.substitute_value(self.symbol_a, self.value)

        self.assertEqual(True, ret_val)
        self.assertEqual(
            self.INT_VALUE,
            self.simple_symb_a.get_actual_argument_value()
        )

    def test_substitute_symbol_incorrect_first_symbol(self):
        not_symbol = 'this string is not a symbol'
        self.assertRaises(
            TypeError,
            self.simple_symb_a.substitute_symbol,
            not_symbol,
            self.symbol_b
        )

    def test_substitute_symbol_incorrect_second_symbol(self):
        not_symbol = 'this string is not a symbol'
        self.assertRaises(
            TypeError,
            self.simple_symb_a.substitute_symbol,
            self.symbol_a,
            not_symbol
        )

    def test_substitute_symbol_to_value_arg(self):
        ret_val = self.simple_val.substitute_symbol(self.symbol_a,
                                                    self.symbol_b)

        self.assertEqual(False, ret_val)
        # Test that content of simple_val has not changed
        self.assertEqual(self.INT_VALUE,
                         self.simple_val.get_actual_argument_value())

    def test_substitute_symbol_to_symbol_arg_with_different_symbol(self):
        ret_val = self.simple_symb_a.substitute_symbol(self.symbol_b,
                                                       self.symbol_a)

        self.assertEqual(False, ret_val)
        # Test that content of simple_symb_a has not changed
        expected = [self.symbol_a]
        self.compare_iterables_content(expected,
                                       self.simple_symb_a.get_symbols())

    def test_substitute_symbol_nominal_case(self):
        ret_val = self.simple_symb_a.substitute_symbol(self.symbol_a,
                                                       self.symbol_b)

        self.assertEqual(True, ret_val)
        self.compare_iterables_content(
            [self.symbol_b],
            self.simple_symb_a.get_symbols()
        )


if __name__ == '__main__':
    unittest.main()