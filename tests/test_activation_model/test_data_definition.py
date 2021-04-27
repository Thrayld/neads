import unittest

import pathlib
import os
import pickle as pkl


from neads.activation_model.data_definition import DataDefinition
from neads.activation_model.symbolic_argument_set import SymbolicArgumentSet
from neads.activation_model.symbolic_objects import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        def f_1(x):  # noqa
            pass

        self.f_1 = f_1

        self.fid = 'my_function'
        self.fid_other = 'other_function'

        self.sym_a = Symbol()
        self.sym_b = Symbol()

        self.sas_f_1__1 = SymbolicArgumentSet(f_1, 1)
        self.sas_f_1__2 = SymbolicArgumentSet(f_1, 2)
        self.sas_f_1__sym_a = SymbolicArgumentSet(f_1, self.sym_a)
        self.sas_f_1__sym_b = SymbolicArgumentSet(f_1, self.sym_b)

    def _check_pickle_dump_load(self, ddf):
        file_name = pathlib.Path('tmp.pkl')

        with open(file_name, 'wb') as f:
            pkl.dump(ddf, f)

        with open(file_name, 'rb') as f:
            ddf_loaded = pkl.load(f)

        self.assertIs(ddf, ddf_loaded)
        os.remove(file_name)

    def test_simple_ddf_survives_pickle(self):
        ddf = DataDefinition.get_instance(self.fid, self.sas_f_1__1)

        self._check_pickle_dump_load(ddf)

    def test_recursive_ddf_survives_pickle(self):
        ddf = DataDefinition.get_instance(self.fid, self.sas_f_1__1)
        ddf_outer = DataDefinition.get_instance(self.fid,
                                                self.sas_f_1__sym_a,
                                                {self.sym_a: ddf})

        self._check_pickle_dump_load(ddf_outer)

    def test_sas_with_remaining_symbols(self):
        self.assertRaises(
            ValueError,
            DataDefinition.get_instance,
            self.fid,
            self.sas_f_1__sym_a
        )

    def test_un_hashable_fid(self):
        self.assertRaises(
            TypeError,
            DataDefinition.get_instance,
            ['un-hashable function_id'],
            self.sas_f_1__1
        )

    def test_un_hashable_sas(self):
        sas = SymbolicArgumentSet(self.f_1, ['something un-hashable'])

        self.assertRaises(
            TypeError,
            DataDefinition.get_instance,
            self.fid,
            sas
        )

    def test_same_fid_different_sas(self):
        ddf_1 = DataDefinition.get_instance(self.fid, self.sas_f_1__1)
        ddf_2 = DataDefinition.get_instance(self.fid, self.sas_f_1__2)

        self.assertIsNot(ddf_1, ddf_2)

    def test_different_fid_same_sas(self):
        ddf_1 = DataDefinition.get_instance(self.fid, self.sas_f_1__1)
        ddf_2 = DataDefinition.get_instance(self.fid_other, self.sas_f_1__1)

        self.assertIsNot(ddf_1, ddf_2)

    def test_same_fid_same_sas_different_recursive_ddf(self):
        ddf_1 = DataDefinition.get_instance(self.fid, self.sas_f_1__1)
        ddf_2 = DataDefinition.get_instance(self.fid, self.sas_f_1__2)

        ddf_outer_1 = DataDefinition.get_instance(
            self.fid, self.sas_f_1__sym_a, {self.sym_a: ddf_1}
        )
        ddf_outer_2 = DataDefinition.get_instance(
            self.fid, self.sas_f_1__sym_a, {self.sym_a: ddf_2}
        )

        self.assertIsNot(ddf_outer_1, ddf_outer_2)

    def test_same_fid_same_sas(self):
        ddf_1 = DataDefinition.get_instance(self.fid, self.sas_f_1__1)
        ddf_2 = DataDefinition.get_instance(self.fid, self.sas_f_1__1)

        self.assertIs(ddf_1, ddf_2)

    def test_same_fid_sas_with_different_symbol_but_same_recursive_dff(self):
        ddf_1 = DataDefinition.get_instance(self.fid, self.sas_f_1__1)
        ddf_2 = DataDefinition.get_instance(self.fid, self.sas_f_1__1)

        ddf_outer_1 = DataDefinition.get_instance(
            self.fid, self.sas_f_1__sym_a, {self.sym_a: ddf_1}
        )
        ddf_outer_2 = DataDefinition.get_instance(
            self.fid, self.sas_f_1__sym_b, {self.sym_b: ddf_2}
        )

        self.assertIs(ddf_outer_1, ddf_outer_2)


if __name__ == '__main__':
    unittest.main()
