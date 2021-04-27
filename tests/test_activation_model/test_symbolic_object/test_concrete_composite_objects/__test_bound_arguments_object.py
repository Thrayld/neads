import unittest
import inspect

from neads.activation_model.symbolic_objects import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        def f(x, y):  # noqa
            pass

        def g(*args, **kwargs):  # noqa
            pass

        def h(x, y, z):  # noqa
            pass

        self.f_x_y = f
        self.g_args_kwargs = g
        self.h_x_y_z = h

        self.bounded_f_1_2 = inspect.signature(f).bind(1, 2)

        self.symbol_a = Symbol()
        self.symbol_b = Symbol()
        
        self.val_1 = Value(1)
        self.val_2 = Value(2)

        self.list_ab = ListObject(self.symbol_a, self.symbol_b)
        
    def test_init_with_signature(self):
        sig = inspect.signature(self.f_x_y)

        sas = BoundArgumentObject(sig, self.val_1, self.val_2)
        actual = sas.get_value()

        self.assertEqual(self.bounded_f_1_2, actual)
        
    def test_init_bad_types(self):
        self.assertRaises(
            TypeError,
            BoundArgumentObject,
            self.f_x_y, 1  
        )

    def test_init_with_no_signature_nor_callable(self):
        self.assertRaises(
            TypeError,
            BoundArgumentObject,
            'really not a signature nor callable',
            self.val_1
        )

    def test_init_wrong_number_of_positional_arguments(self):
        self.assertRaises(
            TypeError,
            BoundArgumentObject,
            self.f_x_y,
            self.val_1, self.val_1, self.val_1
        )

    def test_init_wrong_keyword_argument(self):
        self.assertRaises(
            TypeError,
            BoundArgumentObject,
            self.f_x_y,
            self.val_1, self.val_2, z=self.val_1
        )

    def test_init_trying_to_reach_positional_only_argument(self):
        def f(x, /):  # noqa
            pass

        self.assertRaises(
            TypeError,
            BoundArgumentObject,
            f,
            x=self.val_1
        )

    def test_get_symbols_no_symbols(self):
        sas = BoundArgumentObject(self.f_x_y, self.val_1, self.val_2)

        actual = sas.get_symbols()

        expected = []
        self.assertCountEqual(expected, actual)

    def test_get_symbols_some_symbols(self):
        sas = BoundArgumentObject(self.f_x_y, self.symbol_a, self.list_ab)

        actual = sas.get_symbols()

        expected = [self.symbol_a, self.symbol_b]
        self.assertCountEqual(expected, actual)
        
    def test_substitute(self):
        sas = BoundArgumentObject(self.f_x_y, self.symbol_a, self.val_2)

        actual = sas.substitute(self.symbol_a, self.val_1).get_value()

        self.assertEqual(self.bounded_f_1_2, actual)

    def test_substitute_no_replacement(self):
        sas = BoundArgumentObject(self.f_x_y, self.symbol_a, self.val_2)

        actual = sas.substitute(self.symbol_a, self.val_1).get_value()

        self.assertIs(sas, actual)

    def test_get_value_copy_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_a: list_,
            self.symbol_b: list_
        }

        sas = BoundArgumentObject(self.h_x_y_z,
                                  self.symbol_a, self.symbol_a, self.symbol_b)
        actual = sas.get_value(to_subs).args

        self.assertIsNot(list_, actual[0])
        self.assertIs(actual[0], actual[1])
        self.assertIsNot(actual[0], actual[2])

    def test_get_value_copy_not_share(self):
        list_ = [1]
        to_subs = {
            self.symbol_a: list_,
            self.symbol_b: list_
        }

        sas = BoundArgumentObject(self.h_x_y_z,
                                  self.symbol_a, self.symbol_a, self.symbol_b)
        actual = sas.get_value(to_subs, share=False).args

        self.assertIsNot(list_, actual[0])
        self.assertIsNot(actual[0], actual[1])
        self.assertIsNot(actual[0], actual[2])

    def test_get_value_not_copy(self):
        list_ = [1]
        to_subs = {
            self.symbol_a: list_,
            self.symbol_b: list_
        }

        sas = BoundArgumentObject(self.h_x_y_z,
                                  self.symbol_a, self.symbol_a, self.symbol_b)
        actual = sas.get_value(to_subs, copy=False).args

        self.assertIs(list_, actual[0])
        self.assertIs(actual[0], actual[1])
        self.assertIs(actual[0], actual[2])
    
    def test_get_value_with_unsubstituted_symbols(self):
        sas = BoundArgumentObject(self.f_x_y, self.symbol_a, self.val_2)

        self.assertRaises(
            SymbolicObjectException,
            sas.get_value
        )

    def test_eq_keyword_or_positional_arguments(self):
        sas_1 = BoundArgumentObject(self.f_x_y, self.val_1, self.val_2)
        sas_2 = BoundArgumentObject(self.f_x_y, x=self.val_1, y=self.val_2)

        self.assertEqual(sas_1, sas_2)

    def test_eq_args_vs_kwargs(self):
        sas_1 = BoundArgumentObject(self.g_args_kwargs, self.val_1, self.val_2)
        sas_2 = BoundArgumentObject(self.g_args_kwargs,
                                    x=self.val_1, y=self.val_2)

        self.assertNotEqual(sas_1, sas_2)

    def test_eq_with_default_args(self):
        def f(x, y=2):  # noqa
            pass

        sas_1 = BoundArgumentObject(f, self.val_1)
        sas_2 = BoundArgumentObject(f, self.val_1, self.val_2)

        self.assertEqual(sas_1, sas_2)
    
    def test_hash_constant_in_two_calls(self):
        sas = BoundArgumentObject(self.f_x_y, self.val_1, self.val_2)

        self.assertEqual(hash(sas), hash(sas))

    def test_hash_same_for_equal_objects(self):
        sas_1 = BoundArgumentObject(self.f_x_y, self.val_1, self.val_2)
        sas_2 = BoundArgumentObject(self.f_x_y, x=self.val_1, y=self.val_2)

        self.assertEqual(hash(sas_1), hash(sas_2))

    def test_hash_for_different_objects(self):
        sas_1 = BoundArgumentObject(self.g_args_kwargs, self.val_1, self.val_2)
        sas_2 = BoundArgumentObject(self.g_args_kwargs,
                                    x=self.val_1, y=self.val_2)

        self.assertNotEqual(hash(sas_1), hash(sas_2))
    

if __name__ == '__main__':
    unittest.main()
