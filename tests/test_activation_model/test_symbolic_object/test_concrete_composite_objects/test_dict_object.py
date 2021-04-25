import unittest

from neads.activation_model.symbolic_objects import *


class TestDictObjectFlat(unittest.TestCase):
    def setUp(self) -> None:
        self.int = 0
        self.string = 'key'
        self.value_int = Value(self.int)
        self.value_string = Value(self.string)

        self.symbol_1 = Symbol()
        self.symbol_2 = Symbol()

        self.dict_object = DictObject(
            {
                self.value_int: self.symbol_1,
                self.value_string: self.symbol_2
            }
        )

    def test_init_bad_types(self):
        self.assertRaises(
            TypeError,
            DictObject,
            {self.string: self.value_int}
        )

    def test_substitute(self):
        value_10 = Value(10)
        value_15 = Value(15)
        to_subs = {
            self.symbol_1: value_10,
            self.symbol_2: value_15
        }
        expected = {
            self.int: 10,
            self.string: 15
        }

        after_subs = self.dict_object.substitute(to_subs)
        actual = after_subs.get_value()

        self.assertEqual(expected, actual)

    def test_get_symbols(self):
        expected = [self.symbol_1, self.symbol_2]

        actual = self.dict_object.get_symbols()

        self.assertCountEqual(expected, actual)

    # def test_get_value_with_invalid_type_for_key(self):
    #     ### The test cannot work, as [1] in Value is not hashable and that
    #     ### is OK
    #     TODO: add it to documentation
    #
    #     bad_value = Value([1])
    #     dict_ = {bad_value: self.value_int}
    #     dict_object = DictObject(dict_)
    #
    #     self.assertRaises(
    #         TypeError,
    #         dict_object.get_value
    #     )

    def test_get_value_with_symbols_left(self):
        self.assertRaises(
            SymbolicObjectException,
            self.dict_object.get_value
        )

    def test_get_value_copy_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_1: list_,
        }

        after_subs = self.dict_object.substitute(self.symbol_2, self.symbol_1)
        actual = after_subs.get_value(to_subs)

        self.assertIsNot(list_, actual[self.int])
        self.assertIs(actual[self.int], actual[self.string])

    def test_get_value_copy_not_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_1: list_,
        }

        after_subs = self.dict_object.substitute(self.symbol_2, self.symbol_1)
        actual = after_subs.get_value(to_subs, share=False)

        self.assertIsNot(list_, actual[self.int])
        self.assertIsNot(actual[self.int], actual[self.string])

    def test_get_value_not_copy(self):
        list_ = [1]
        to_subs = {
            self.symbol_1: list_,
        }

        after_subs = self.dict_object.substitute(self.symbol_2, self.symbol_1)
        actual = after_subs.get_value(to_subs, copy=False)

        self.assertIs(list_, actual[self.int])
        self.assertIs(actual[self.int], actual[self.string])

    def test_get_value_without_symbols(self):
        dict_object = DictObject({self.value_string: self.value_int})
        expected = {self.string: self.int}

        actual = dict_object.get_value()

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_different_object(self):
        expected = False

        actual = self.dict_object == self.symbol_1

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_same_structured_dict(self):
        other = DictObject(
            {
                self.value_string: self.symbol_2,
                self.value_int: self.symbol_1
            }
        )
        expected = True

        actual = self.dict_object == other

        self.assertEqual(expected, actual)

    def test_eq_comparison_with_different_dict(self):
        other = DictObject({self.value_string: self.value_int})
        expected = False

        actual = self.dict_object == other

        self.assertEqual(expected, actual)

    def test_hash_constant_in_two_calls(self):
        self.assertEqual(hash(self.dict_object), hash(self.dict_object))

    def test_hash_same_for_equal_objects(self):
        other = DictObject(
            {
                self.value_string: self.symbol_2,
                self.value_int: self.symbol_1
            }
        )

        self.assertEqual(hash(self.dict_object), hash(other))

    def test_hash_for_different_objects(self):
        other = DictObject({self.symbol_1: self.value_int})

        self.assertNotEqual(hash(self.dict_object), hash(other))


class TestDictObjectNested(unittest.TestCase):
    def setUp(self) -> None:
        self.int = 0
        self.string = 'key'
        self.value_int = Value(self.int)
        self.value_string = Value(self.string)
        self.symbol_1 = Symbol()
        self.symbol_2 = Symbol()

        self.inner = DictObject({self.value_int: self.symbol_1})
        self.outer = DictObject({self.symbol_2: self.inner})

    def test_substitute_inner_not_affected(self):
        expected_inner_symbols = [self.symbol_1]

        self.outer.substitute(self.symbol_1, self.value_int)

        actual_inner_symbols = self.inner.get_symbols()
        self.assertCountEqual(expected_inner_symbols, actual_inner_symbols)

    def test_substitute_and_get_value_nominal(self):
        to_subs = {
            self.symbol_1: self.value_int,
            self.symbol_2: self.value_string
        }
        expected = {
            self.string: {self.int: self.int}
        }

        actual = self.outer.substitute(to_subs).get_value()

        self.assertEqual(expected, actual)

    def test_get_value_with_symbols(self):
        self.assertRaises(
            SymbolicObjectException,
            self.outer.get_value
        )

    def get_symbols(self):
        expected = [self.symbol_1, self.symbol_2]

        actual = self.outer.get_symbols()

        self.assertCountEqual(expected, actual)

    def test_eq_different_structure(self):
        other_dict_object = DictObject({})
        expected = False

        actual = self.outer == other_dict_object

        self.assertEqual(expected, actual)

    def test_eq_same_structure(self):
        other_inner = DictObject({self.value_int: self.symbol_1})
        other_outer = DictObject({self.symbol_2: other_inner})
        expected = True

        actual = self.outer == other_outer

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
