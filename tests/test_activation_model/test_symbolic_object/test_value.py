import unittest

import copy

from neads.activation_model.symbolic_objects import *


class TestSymbol(unittest.TestCase):
    def setUp(self) -> None:
        self.symbol = Symbol()
        self.int_value = 0
        self.value = Value(self.int_value)
        self.diff_value = Value(self.int_value + 1)

        self.nested_lists = [1, [2, 3]]

    def test_init_immutability_with_nested_lists(self):
        """Content of Value does not change, if we later change input object."""
        expected = copy.deepcopy(self.nested_lists)
        value_nested_lists = Value(self.nested_lists)
        result_before = value_nested_lists.get_value()

        # Change input value a get result now
        self.nested_lists[1].append(4)
        result_after = value_nested_lists.get_value()

        # Both results must agree with expected
        self.assertEqual(expected, result_before)
        self.assertEqual(expected, result_after)

    def test_substitute(self):
        after_subs = self.value.substitute(self.symbol, self.diff_value)

        self.assertIs(self.value, after_subs)

    def test_get_symbols(self):
        expected = []

        actual = self.value.get_symbols()

        self.assertCountEqual(expected, actual)

    def test_get_value_simple_object(self):
        actual = self.value.get_value()

        self.assertEqual(self.int_value, actual)

    def test_get_value_immutability_with_nested_lists(self):
        value_nested_lists = Value(self.nested_lists)

        # Get values to later alter them and see changes
        result_1 = value_nested_lists.get_value()
        result_2 = value_nested_lists.get_value()

        # Now they should agree
        self.assertEqual(self.nested_lists, result_1)
        self.assertEqual(self.nested_lists, result_2)
        self.assertEqual(result_1, result_2)

        # Change one result
        result_2[1].append(4)

        # Change should be local for `result_2`
        self.assertEqual(self.nested_lists, result_1)
        self.assertNotEqual(self.nested_lists, result_2)
        self.assertNotEqual(result_1, result_2)

    def test_eq_comparison_with_self(self):
        expected = True

        actual = self.value == self.value

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_eq_values(self):
        first_value = Value([1, [2, 3]])
        second_value = Value([1, [2, 3]])
        expected = True

        actual = first_value == second_value

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_different_value(self):
        expected = False

        actual = self.value == self.diff_value

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
