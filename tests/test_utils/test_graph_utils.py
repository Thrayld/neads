import unittest

import neads.utils.graph_utils as graph_utils
from neads.activation_model import ActivationGraph

import tests.my_test_utilities.arithmetic_plugins as ar_plugins


class TestGraphUtils(unittest.TestCase):
    def test_get_result_activation_different_number_of_result_act(self):
        ag = ActivationGraph(2)
        ag.add_activation(ar_plugins.const, ag.inputs[0])
        ag.add_activation(ar_plugins.const, ag.inputs[1])

        self.assertRaises(
            ValueError,
            graph_utils.get_result_activation,
            ag
        )

    def test_get_result_activation_one_result_act(self):
        ag = ActivationGraph(2)
        act_1 = ag.add_activation(ar_plugins.const, ag.inputs[0])
        act_2 = ag.add_activation(ar_plugins.const, act_1.symbol)

        actual = graph_utils.get_result_activation(ag)

        self.assertIs(act_2, actual)

if __name__ == '__main__':
    unittest.main()
