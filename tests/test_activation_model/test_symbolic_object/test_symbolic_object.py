import unittest

from neads.activation_model.symbolic_objects import Symbol, Value, ListObject


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

    def test_get_value_3_args(self):
        self.assertRaises(
            ValueError,
            self.test_object.get_value,
            self.symbol_1,
            1,
            1
        )

    def test_substitute_2_args_first_not_symbol(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            self.value_1,
            self.value_2
        )

    def test_get_value_2_args_first_not_symbol(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            self.value_1,
            2
        )

    def test_substitute_2_args_second_not_symbolic_object(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            self.symbol_1,
            'not_symbolic_object'
        )

    def test_get_value_2_args_second_not_symbolic_object(self):
        actual = self.symbol_1.get_value(self.symbol_1, 'not_symbolic_object')

        expected = 'not_symbolic_object'
        self.assertEqual(expected, actual)

    def test_substitute_1_args_not_dict_not_iterable(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            0
        )

    def test_get_value_1_args_not_dict_not_iterable(self):
        self.assertRaises(
            TypeError,
            self.test_object.get_value,
            0
        )

    def test_substitute_1_args_dict_not_symbol_as_key(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            {self.value_1: self.value_2}
        )

    def test_get_value_1_args_dict_not_symbol_as_key(self):
        self.assertRaises(
            TypeError,
            self.test_object.get_value,
            {self.value_1: self.value_2}
        )

    def test_substitute_1_args_dict_not_symbolic_object_as_value(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            {self.symbol_1: 'not_symbolic_object'}
        )

    def test_get_value_1_args_dict_not_symbolic_object_as_value(self):
        actual = self.symbol_1.get_value({self.symbol_1: 'not_symbolic_object'})

        expected = 'not_symbolic_object'
        self.assertEqual(expected, actual)

    def test_substitute_1_args_iterable_not_pairs(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            [self.symbol_1, self.value_1]
        )

    def test_get_value_1_args_iterable_not_pairs(self):
        self.assertRaises(
            TypeError,
            self.test_object.get_value,
            [self.symbol_1, self.value_1]
        )

    def test_substitute_1_args_iterable_not_symbol_in_pair(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            [(self.value_1, self.value_2)]
        )

    def test_get_value_1_args_iterable_not_symbol_in_pair(self):
        self.assertRaises(
            TypeError,
            self.test_object.get_value,
            [(self.value_1, self.value_2)]
        )

    def test_substitute_1_args_iterable_not_symbolic_object_in_pair(self):
        self.assertRaises(
            TypeError,
            self.test_object.substitute,
            [(self.symbol_1, 'not_symbolic_object')]
        )

    def test_get_value_1_args_iterable_not_symbolic_object_in_pair(self):
        iterable = [(self.symbol_1, 'not_symbolic_object')]

        actual = self.symbol_1.get_value(iterable)

        expected = 'not_symbolic_object'
        self.assertEqual(expected, actual)

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

    def test_get_value_1_args_iterable_more_values_for_one_symbol(self):
        subs_iterable = [
            (self.symbol_1, self.value_1),
            (self.symbol_1, self.value_2)
        ]

        self.assertRaises(
            ValueError,
            self.test_object.get_value,
            subs_iterable
        )

    def test_substitute_2_args_ok(self):
        one_subs = self.test_object.substitute(self.symbol_1, self.value_1)
        two_subs = one_subs.substitute(self.symbol_2, self.value_2)
        actual = two_subs.get_value()

        expected = [1, 2]
        self.assertEqual(expected, actual)

    def test_substitute_1_args_dict_ok(self):
        subs_dict = {
            self.symbol_1: self.value_1,
            self.symbol_2: self.value_2
        }

        after_subs = self.test_object.substitute(subs_dict)
        actual = after_subs.get_value()

        expected = [1, 2]
        self.assertEqual(expected, actual)

    def test_get_value_1_args_dict_ok(self):
        subs_dict = {
            self.symbol_1: 1,
            self.symbol_2: 2
        }

        actual = self.test_object.get_value(subs_dict)

        expected = [1, 2]
        self.assertEqual(expected, actual)

    def test_substitute_1_args_iterable_ok(self):
        subs_iterable = [
            (self.symbol_1, self.value_1),
            (self.symbol_2, self.value_2)
        ]

        after_subs = self.test_object.substitute(subs_iterable)
        actual = after_subs.get_value()

        expected = [1, 2]
        self.assertEqual(expected, actual)

    def test_get_value_1_args_iterable_ok(self):
        subs_iterable = [
            (self.symbol_1, 1),
            (self.symbol_2, 1)
        ]

        actual = self.test_object.get_value(subs_iterable)

        expected = [1, 2]
        self.assertEqual(expected, actual)


class TestSymbolicObjectGetValueSharing(unittest.TestCase):
    def setUp(self) -> None:
        self.symbol_1 = Symbol()
        self.symbol_2 = Symbol()

        self.list_ = [1, 2]
        self.expected = [self.list_, self.list_]

        self.test_object = ListObject(self.symbol_1, self.symbol_2)

    def test_get_value_with_copy_and_share(self):
        subs_iterable = [
            (self.symbol_1, self.list_)
        ]

        after_subs = self.test_object.substitute(self.symbol_2, self.symbol_1)
        actual = after_subs.get_value(subs_iterable)

        self.assertEqual(self.expected, actual)

        self.assertIsNot(self.list_, actual[0])
        self.assertIsNot(self.list_, actual[1])

        # Copy is `self.list_` is shared
        self.assertIs(actual[0], actual[1])

    def test_get_value_with_copy_and_share_but_different_symbols(self):
        subs_iterable = [
            (self.symbol_1, self.list_),
            (self.symbol_2, self.list_)
        ]

        actual = self.test_object.get_value(subs_iterable)

        self.assertEqual(self.expected, actual)

        self.assertIsNot(self.list_, actual[0])
        self.assertIsNot(self.list_, actual[1])

        # Copy is `outer_list` is NOT shared, because the original Symbols
        # were different
        # Compare with the test above
        self.assertIsNot(actual[0], actual[1])

    def test_get_value_with_copy_and_not_share(self):
        subs_iterable = [
            (self.symbol_1, self.list_)
        ]

        after_subs = self.test_object.substitute(self.symbol_2, self.symbol_1)
        actual = after_subs.get_value(subs_iterable, share=False)

        self.assertEqual(self.expected, actual)

        self.assertIsNot(self.list_, actual[0])
        self.assertIsNot(self.list_, actual[1])

        # Copy is `outer_list` is NOT shared
        self.assertIsNot(actual[0], actual[1])

    def test_get_value_without_copy(self):
        subs_iterable = [
            (self.symbol_1, self.list_),
            (self.symbol_2, self.list_)
        ]

        actual = self.test_object.get_value(subs_iterable, copy=False)

        self.assertEqual(self.expected, actual)

        self.assertIs(self.list_, actual[0])
        self.assertIs(self.list_, actual[1])


if __name__ == '__main__':
    unittest.main()
