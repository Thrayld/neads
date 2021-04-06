import unittest

from neads.symbolic_argument import *


class TestSimpleArgument(unittest.TestCase):

    def setUp(self) -> None:
        self.INT_VALUE = 100
        self.symbol_a = Symbol('a')
        self.symbol_b = Symbol('b')
        self.value = Value(self.INT_VALUE)
        self.simple_symb_a = SimpleArgument(self.symbol_a)
        self.simple_val = SimpleArgument(self.value)

    def test_init_with_wrong_type(self):
        self.assertRaises(
            TypeError,
            SimpleArgument,
            'this is not Symbol nor Value'
        )

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
        self.assertCountEqual(expected_iterable, actual_iterable)

    def test_get_symbols_with_value(self):
        expected_iterable = []
        actual_iterable = self.simple_val.get_symbols()
        self.assertCountEqual(expected_iterable, actual_iterable)

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
        self.assertCountEqual(expected, self.simple_symb_a.get_symbols())

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
        self.assertCountEqual(expected, self.simple_symb_a.get_symbols())

    def test_substitute_symbol_nominal_case(self):
        ret_val = self.simple_symb_a.substitute_symbol(self.symbol_a,
                                                       self.symbol_b)

        self.assertEqual(True, ret_val)
        self.assertCountEqual(
            [self.symbol_b],
            self.simple_symb_a.get_symbols()
        )


class TestListArgument(unittest.TestCase):

    def setUp(self) -> None:
        self.SYMBOL_SIGNS = [0, 1, 2]
        self.INT_VALUES = [10, 11, 12]
        self.symbols = [Symbol(sign) for sign in self.SYMBOL_SIGNS]
        self.values = [Value(val) for val in self.INT_VALUES]
        self.symbol_simple_args = [SimpleArgument(s) for s in self.symbols]
        self.value_simple_args = [SimpleArgument(v) for v in self.values]

        self.used_symbols_indices = (0, 1, 0)
        self.symbol_symbolic_args_010 = [
            self.symbol_simple_args[i] for i in self.used_symbols_indices
        ]
        self.list_arg_010 = ListArgument(
            self.symbol_symbolic_args_010
        )

    def test_init_with_symbolic_arguments(self):
        list_arg = ListArgument(
            *self.value_simple_args
        )
        self.assertEqual(
            self.INT_VALUES,
            list_arg.get_actual_argument_value()
        )

    def test_init_with_one_sequence_non_symbolic_argument(self):
        list_arg = ListArgument(
            self.value_simple_args
        )
        self.assertEqual(
            self.INT_VALUES,
            list_arg.get_actual_argument_value()
        )

    @unittest.skip(reason='Currently, we do not have a subtype of both '
                          'Sequence and SymbolicArgument')
    def test_init_with_one_sequence_and_symbolic_argument(self):
        raise NotImplementedError()

    def test_init_with_not_symbolic_argument(self):
        self.assertRaises(
            TypeError,
            ListArgument,
            self.symbol_simple_args[0],
            1
        )

    def test_init_with_sequence_of_non_symbolic_arguments(self):
        self.assertRaises(
            TypeError,
            ListArgument,
            'sequence of non-SymbolicArguments'
        )

    def test_substitute_value_nominal_case(self):
        # --- Substitution for symbol 0
        flag_symbol_0 = self.list_arg_010.substitute_value(self.symbols[0],
                                                           self.values[0])

        # --- Test for symbol 0
        # Substitution occurred
        self.assertEqual(True, flag_symbol_0)
        # Just symbol 1 is now present
        expected = [self.symbols[1]]
        self.assertCountEqual(expected, self.list_arg_010.get_symbols())

        # --- Substitution for symbol 1
        flag_symbol_0 = self.list_arg_010.substitute_value(self.symbols[1],
                                                           self.values[1])

        # --- Test for symbol 1
        # Substitution occurred
        self.assertEqual(True, flag_symbol_0)
        # No symbol is present
        expected = []
        self.assertCountEqual(expected, self.list_arg_010.get_symbols())

        # --- Test final result
        expected = [self.INT_VALUES[0], self.INT_VALUES[1], self.INT_VALUES[0]]
        self.assertSequenceEqual(
            expected,
            self.list_arg_010.get_actual_argument_value()
        )

    def test_substitute_value_non_present_symbol(self):
        ret_val = self.list_arg_010.substitute_value(self.symbols[2],
                                                     self.values[0])

        self.assertEqual(False, ret_val)
        # Test that symbols of list_arg has not changed
        expected = [self.symbols[0], self.symbols[1]]
        self.assertCountEqual(
            expected,
            self.list_arg_010.get_symbols()
        )

    def test_substitute_symbol_nominal_case(self):
        ret_val = self.list_arg_010.substitute_symbol(self.symbols[0],
                                                      self.symbols[2])

        self.assertEqual(True, ret_val)
        # Just symbol 1 is now present
        expected = [self.symbols[1], self.symbols[2]]
        self.assertCountEqual(expected, self.list_arg_010.get_symbols())

    def test_substitute_symbol_non_present_symbol(self):
        ret_val = self.list_arg_010.substitute_symbol(self.symbols[2],
                                                      self.symbols[0])

        self.assertEqual(False, ret_val)
        # Test that symbols of list_arg has not changed
        expected = [self.symbols[0], self.symbols[1]]
        self.assertCountEqual(
            expected,
            self.list_arg_010.get_symbols()
        )

    def test_get_symbols_without_symbols(self):
        list_arg = ListArgument()
        self.assertCountEqual([], list_arg.get_symbols())

    def test_get_symbols_with_some_symbols(self):
        expected = [self.symbols[0], self.symbols[1]]
        actual = self.list_arg_010.get_symbols()
        self.assertCountEqual(expected, actual)

    def test_get_actual_argument_value_with_symbols(self):
        self.assertRaises(
            SymbolicArgumentException,
            self.list_arg_010.get_actual_argument_value
        )

    def test_get_actual_argument_value_nominal_case(self):
        list_arg = ListArgument(self.value_simple_args)
        expected = self.INT_VALUES
        actual = list_arg.get_actual_argument_value()
        self.assertSequenceEqual(expected, actual)

    # TODO: add test cases with nested lists


if __name__ == '__main__':
    unittest.main()
