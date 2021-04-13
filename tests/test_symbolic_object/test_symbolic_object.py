import unittest

from neads.symbolic_objects import Symbol, Value, SymbolicObjectException, \
    ListObject


class TestSymbolicObject(unittest.TestCase):
    """Test implementation of error checking in substitute on ListObject."""

    def setUp(self) -> None:
        self.symbol_1 = Symbol()
        self.symbol_2 = Symbol()
        self.value_1 = Value(1)
        self.value_2 = Value(2)

        self.test_object = ListObject(self.symbol_1, self.symbol_2)

    def test_substitute_3_args(self):
        self.assertRaises(
            ValueError,
            self.test_object.substitute,
            self.symbol_1,
            self.value_1,
            self.value_1
        )

    def test_substitute_2_args_first_not_symbol(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            self.value_1,
            self.value_2
        )

    def test_substitute_2_args_second_not_symbolic_object(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            self.symbol_1,
            'not_symbolic_object'
        )

    def test_substitute_1_args_not_dict_not_iterable(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            0
        )

    def test_substitute_1_args_dict_not_symbol_as_key(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            {self.value_1: self.value_2}
        )

    def test_substitute_1_args_dict_not_symbolic_object_as_value(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            {self.symbol_1: 'not_symbolic_object'}
        )

    def test_substitute_1_args_iterable_not_pairs(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            [self.symbol_1, self.value_1]
        )

    def test_substitute_1_args_iterable_not_symbol_in_pair(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            [(self.value_1, self.value_2)]
        )

    def test_substitute_1_args_iterable_not_symbolic_object_in_pair(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            [(self.symbol_1, 'not_symbolic_object')]
        )

    def test_substitute_1_args_iterable_more_values_for_one_symbol(self):
        subs_iterable = [
            (self.symbol_1, self.value_1),
            (self.symbol_1, self.value_2)
        ]

        self.assertRaises(
            ValueError,
            self.test_object.substitute,
            subs_iterable
        )

    def test_substitute_2_args_ok(self):
        one_subs = self.test_object.substitute(self.symbol_1, self.value_1)
        two_subs = one_subs.substitute(self.symbol_2, self.value_2)
        result = two_subs.get_value()

        expected = [1, 2]
        self.assertEqual(expected, result)

    def test_substitute_1_args_dict_ok(self):
        subs_dict = {
            self.symbol_1: self.value_1,
            self.symbol_2: self.value_2
        }

        after_subs = self.test_object.substitute(subs_dict)
        result = after_subs.get_value()

        expected = [1, 2]
        self.assertEqual(expected, result)

    def test_substitute_1_args_iterable_ok(self):
        subs_iterable = [
            (self.symbol_1, self.value_1),
            (self.symbol_2, self.value_2)
        ]

        after_subs = self.test_object.substitute(subs_iterable)
        result = after_subs.get_value()

        expected = [1, 2]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
