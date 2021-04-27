import unittest

from neads.activation_model.symbolic_objects import *


class TestListObjectFlat(unittest.TestCase):
    def setUp(self) -> None:
        self.symbol_1 = Symbol()
        self.symbol_2 = Symbol()
        self.int_value = 0
        self.value = Value(self.int_value)

        self.list_object = ListObject(
            self.symbol_1,
            self.symbol_1,
            self.symbol_2,
            self.value
        )

    def test_init_bad_types(self):
        self.assertRaises(
            TypeError,
            ListObject,
            0
        )

    def test_substitute_all_at_once(self):
        value_10 = Value(10)
        value_15 = Value(15)
        to_subs = {
            self.symbol_1: value_10,
            self.symbol_2: value_15
        }
        expected = [10, 10, 15, self.int_value]

        after_subs = self.list_object.substitute(to_subs)
        actual = after_subs.get_value()

        self.assertEqual(expected, actual)

    def test_substitute_gradually(self):
        value_10 = Value(10)
        value_15 = Value(15)

        after_one_sub = self.list_object.substitute(self.symbol_1, value_10)
        after_two_subs = after_one_sub.substitute(self.symbol_2, value_15)

        # Assertion for `after_one_sub`
        self.assertCountEqual(
            [self.symbol_2],
            after_one_sub.get_symbols()
        )
        self.assertRaises(
            SymbolicObjectException,
            after_one_sub.get_value
        )

        # Assertion for `after_two_subs`
        expected = [10, 10, 15, self.int_value]
        self.assertEqual(
            expected,
            after_two_subs.get_value()
        )

    def test_get_symbols(self):
        expected = [self.symbol_1, self.symbol_2]

        actual = self.list_object.get_symbols()

        self.assertCountEqual(expected, actual)

    def test_get_value_without_symbols(self):
        list_obj = ListObject(self.value, self.value)
        expected = [self.int_value, self.int_value]

        actual = list_obj.get_value()

        self.assertEqual(expected, actual)

    def test_get_value_copy_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_1: list_,
            self.symbol_2: list_
        }

        actual = self.list_object.get_value(to_subs)

        self.assertIsNot(list_, actual[0])
        self.assertIs(actual[0], actual[1])
        self.assertIsNot(actual[0], actual[2])

    def test_get_value_copy_not_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_1: list_,
            self.symbol_2: list_
        }

        actual = self.list_object.get_value(to_subs, share=False)

        self.assertIsNot(list_, actual[0])
        self.assertIsNot(actual[0], actual[1])
        self.assertIsNot(actual[0], actual[2])

    def test_get_value_not_copy(self):
        list_ = [1]
        to_subs = {
            self.symbol_1: list_,
            self.symbol_2: list_
        }

        actual = self.list_object.get_value(to_subs, copy=False)

        self.assertIs(list_, actual[0])
        self.assertIs(actual[0], actual[1])
        self.assertIs(actual[0], actual[2])

    def test_get_value_with_unsubstituted_symbols(self):
        self.assertRaises(
            SymbolicObjectException,
            self.list_object.get_value
        )

    def test_eq_comparison_with_different_symbolic_object(self):
        expected = False

        actual = self.list_object == self.value

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_list_object_with_different_len(self):
        other = ListObject(self.symbol_1, self.symbol_1, self.symbol_2)
        expected = False

        actual = self.list_object == other

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_list_object_with_different_entries(self):
        other = ListObject(
            self.symbol_2,
            self.symbol_1,
            self.symbol_2,
            self.value
        )
        expected = False

        actual = self.list_object == other

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_list_object_with_same_entries(self):
        other = ListObject(
            self.symbol_1,
            self.symbol_1,
            self.symbol_2,
            self.value
        )
        expected = True

        actual = self.list_object == other

        self.assertEqual(expected, actual)

    def test_hash_constant_in_two_calls(self):
        self.assertEqual(hash(self.list_object), hash(self.list_object))

    def test_hash_same_for_equal_objects(self):
        other = ListObject(
            self.symbol_1,
            self.symbol_1,
            self.symbol_2,
            self.value
        )

        self.assertEqual(hash(self.list_object), hash(other))

    def test_hash_for_different_objects(self):
        other = ListObject(self.symbol_1)

        self.assertNotEqual(hash(self.list_object), hash(other))

    def test_getitem(self):
        self.assertIs(self.symbol_1, self.list_object[0])
        self.assertIs(self.symbol_1, self.list_object[1])
        self.assertIs(self.symbol_2, self.list_object[2])
        self.assertIs(self.value, self.list_object[3])

    def test_getitem_slice(self):
        self.assertSequenceEqual(
            [self.symbol_1, self.symbol_1],
            self.list_object[0:2]
        )

    def test_getitem_index_out_of_bounds(self):
        self.assertRaises(
            IndexError,
            self.list_object.__getitem__,
            4
        )

    def test_len(self):
        actual = len(self.list_object)

        expected = 4
        self.assertIs(expected, actual)

    def test_len_empty(self):
        list_ = ListObject()

        actual = len(list_)

        expected = 0
        self.assertIs(expected, actual)

class TestListObjectNested(unittest.TestCase):
    def setUp(self) -> None:
        self.int_value = 0
        self.value = Value(self.int_value)
        self.symbol_1 = Symbol()
        self.symbol_2 = Symbol()

        self.inner = ListObject(self.symbol_1, self.value)
        self.outer = ListObject(self.symbol_2, self.inner)

    def test_substitute_inner_not_affected(self):
        expected_inner_symbols = [self.symbol_1]

        self.outer.substitute(self.symbol_1, self.value)

        actual_inner_symbols = self.inner.get_symbols()
        self.assertCountEqual(expected_inner_symbols, actual_inner_symbols)

    def test_substitute_and_get_value_nominal(self):
        value_10 = Value(10)
        value_15 = Value(15)
        expected = [15, [10, self.int_value]]

        after_one = self.outer.substitute(self.symbol_1, value_10)
        after_two = after_one.substitute(self.symbol_2, value_15)
        actual = after_two.get_value()

        self.assertEqual(expected, actual)

    def test_get_symbols(self):
        expected = [self.symbol_1, self.symbol_2]

        actual = self.outer.get_symbols()

        self.assertCountEqual(expected, actual)

    def test_get_value_without_symbols(self):
        values = [Value(i) for i in range(3)]
        inner = ListObject(values[0], values[1])
        outer = ListObject(values[2], inner)
        expected = [2, [0, 1]]

        actual = outer.get_value()

        self.assertEqual(expected, actual)

    def test_get_value_with_symbols(self):
        self.assertRaises(
            SymbolicObjectException,
            self.outer.get_value
        )

    def test_eq_different_structure(self):
        other_inner = ListObject(self.symbol_1)
        other_outer = ListObject(self.symbol_2, other_inner)
        expected = False

        actual = self.outer == other_outer

        self.assertEqual(expected, actual)

    def test_eq_same_structure(self):
        other_inner = ListObject(self.symbol_1, self.value)
        other_outer = ListObject(self.symbol_2, other_inner)
        expected = True

        actual = self.outer == other_outer

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
