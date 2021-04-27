import unittest
import inspect

from neads.activation_model.symbolic_argument_set import SymbolicArgumentSet
from neads.activation_model.symbolic_objects import *


class TestSymbolicArgumentSet(unittest.TestCase):
    def setUp(self) -> None:
        def f(x, y):
            pass

        def g(*args, **kwargs):
            pass

        def h(x, y, z):
            pass

        self.f_x_y = f
        self.g_args_kwargs = g
        self.h_x_y_z = h

        self.bounded_f_1_2 = inspect.signature(f).bind(1, 2)

        self.symbol_a = Symbol()
        self.symbol_b = Symbol()

        self.list_ab = ListObject(self.symbol_a, self.symbol_b)

    def test_init_with_signature(self):
        sig = inspect.signature(self.f_x_y)

        sas = SymbolicArgumentSet(sig, 1, 2)
        actual = sas.get_actual_arguments()

        self.assertEqual(self.bounded_f_1_2, actual)

    def test_init_with_no_signature_nor_callable(self):
        self.assertRaises(
            TypeError,
            SymbolicArgumentSet,
            'really not a signature nor callable',
            1, 2, 3
        )

    def test_init_wrong_number_of_positional_arguments(self):
        self.assertRaises(
            TypeError,
            SymbolicArgumentSet,
            self.f_x_y,
            1, 2, 3
        )

    def test_init_wrong_keyword_argument(self):
        self.assertRaises(
            TypeError,
            SymbolicArgumentSet,
            self.f_x_y,
            1, 2, z=2
        )

    def test_init_trying_to_reach_positional_only_argument(self):
        def f(x, /):
            pass

        self.assertRaises(
            TypeError,
            SymbolicArgumentSet,
            f,
            x=1
        )

    def test_get_symbols_no_symbols(self):
        sas = SymbolicArgumentSet(self.f_x_y, 1, 2)

        actual = sas.get_symbols()

        expected = []
        self.assertCountEqual(expected, actual)

    def test_get_symbols_some_symbols(self):
        sas = SymbolicArgumentSet(self.f_x_y, self.symbol_a, self.list_ab)

        actual = sas.get_symbols()

        expected = [self.symbol_a, self.symbol_b]
        self.assertCountEqual(expected, actual)

    def test_substitute_positional_args(self):
        sas = SymbolicArgumentSet(self.f_x_y, self.symbol_a, 2)

        actual = sas.substitute(self.symbol_a, Value(1)).get_actual_arguments()

        self.assertEqual(self.bounded_f_1_2, actual)

    def test_substitute_with_kwargs(self):
        sas = SymbolicArgumentSet(self.g_args_kwargs, x=self.symbol_a)

        actual = sas.substitute(self.symbol_a, Value(1)).get_actual_arguments()

        expected = inspect.signature(self.g_args_kwargs).bind(x=1)
        self.assertEqual(expected, actual)

    def test_substitute_negative_example(self):
        sas = SymbolicArgumentSet(self.f_x_y, self.symbol_a, 2)

        self.assertRaises(
            ValueError,
            sas.substitute,
            Value(1), Value(1), Value(1)
        )

    def test_get_actual_arguments_positive_example(self):
        sas = SymbolicArgumentSet(self.f_x_y, self.symbol_a, 2)

        actual = sas.get_actual_arguments(self.symbol_a, 1)

        self.assertEqual(self.bounded_f_1_2, actual)

    def test_get_actual_arguments_negative_example(self):
        sas = SymbolicArgumentSet(self.f_x_y, self.symbol_a, 2)

        self.assertRaises(
            TypeError,
            sas.get_actual_arguments,
            'really not a symbol',
            10
        )

    def test_get_actual_arguments_function_with_default_arguments(self):
        def f(x, y=2):
            pass

        sas = SymbolicArgumentSet(f, 1)

        actual = sas.get_actual_arguments()

        expected = inspect.signature(f).bind(x=1, y=2)
        self.assertEqual(expected, actual)

    def test_get_value_copy_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_a: list_,
            self.symbol_b: list_
        }

        sas = SymbolicArgumentSet(self.h_x_y_z,
                                  self.symbol_a, self.symbol_a, self.symbol_b)
        actual = sas.get_actual_arguments(to_subs).args

        self.assertIsNot(list_, actual[0])
        self.assertIs(actual[0], actual[1])
        self.assertIsNot(actual[0], actual[2])

    def test_get_value_copy_not_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_a: list_,
            self.symbol_b: list_
        }

        sas = SymbolicArgumentSet(self.h_x_y_z,
                                  self.symbol_a, self.symbol_a, self.symbol_b)
        actual = sas.get_actual_arguments(to_subs, share=False).args

        self.assertIsNot(list_, actual[0])
        self.assertIsNot(actual[0], actual[1])
        self.assertIsNot(actual[0], actual[2])

    def test_get_value_not_copy(self):
        list_ = [1]
        to_subs = {
            self.symbol_a: list_,
            self.symbol_b: list_
        }

        sas = SymbolicArgumentSet(self.h_x_y_z,
                                  self.symbol_a, self.symbol_a, self.symbol_b)
        actual = sas.get_actual_arguments(to_subs, copy=False).args

        self.assertIs(list_, actual[0])
        self.assertIs(actual[0], actual[1])
        self.assertIs(actual[0], actual[2])

    def test_eq_keyword_or_positional_arguments(self):
        sas_1 = SymbolicArgumentSet(self.f_x_y, 1, 2)
        sas_2 = SymbolicArgumentSet(self.f_x_y, x=1, y=2)

        self.assertEqual(sas_1, sas_2)

    def test_eq_ints_vs_symbolic_objects(self):
        values = [Value(i) for i in [1, 2]]
        sas_1 = SymbolicArgumentSet(self.f_x_y, 1, 2)
        sas_2 = SymbolicArgumentSet(self.f_x_y, *values)

        self.assertEqual(sas_1, sas_2)

    def test_eq_args_vs_kwargs(self):
        sas_1 = SymbolicArgumentSet(self.g_args_kwargs, 1, 2)
        sas_2 = SymbolicArgumentSet(self.g_args_kwargs, x=1, y=2)

        self.assertNotEqual(sas_1, sas_2)

    def test_eq_with_default_args(self):
        def f(x, y=2):
            pass

        sas_1 = SymbolicArgumentSet(f, 1)
        sas_2 = SymbolicArgumentSet(f, 1, Value(2))

        self.assertEqual(sas_1, sas_2)


if __name__ == '__main__':
    unittest.main()
