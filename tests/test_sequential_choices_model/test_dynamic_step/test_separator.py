import unittest

from neads.sequential_choices_model import Separator
from neads.activation_model import ActivationGraph, SealedActivationGraph

import tests.my_test_utilities.arithmetic_plugins as ar_plugins


class TestSeparator(unittest.TestCase):
    def test_bad_number_of_inputs(self):
        ag = ActivationGraph(2)
        ag.add_activation(ar_plugins.const, ag.inputs[0])

        self.assertRaises(
            ValueError,
            Separator,
            ag
        )

    def test_bad_number_of_result_activations(self):
        ag = ActivationGraph(2)
        ag.add_activation(ar_plugins.const, ag.inputs[0])
        ag.add_activation(ar_plugins.const, ag.inputs[1])

        self.assertRaises(
            ValueError,
            Separator,
            ag
        )

    def test_graph_has_graph_trigger(self):
        ag = ActivationGraph(1)
        ag.add_activation(ar_plugins.const, ag.inputs[0])
        ag.trigger_method = lambda: None

        self.assertRaises(
            ValueError,
            Separator,
            ag
        )

    def test_graph_has_activation_trigger(self):
        ag = ActivationGraph(1)
        act = ag.add_activation(ar_plugins.const, ag.inputs[0])
        act.trigger_on_descendants = lambda: None

        self.assertRaises(
            ValueError,
            Separator,
            ag
        )

    def test_attach(self):
        ag = ActivationGraph(1)
        ag.add_activation(ar_plugins.const, ag.inputs[0])

        choice = Separator(ag)

        target_graph = SealedActivationGraph()
        act = target_graph.add_activation(ar_plugins.const, 10)

        result_act = choice.attach(target_graph, act)

        self.assertIs(act.children[0], result_act)


if __name__ == '__main__':
    unittest.main()
