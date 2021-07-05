import unittest

from neads.sequential_choices_model import Extractor
from neads.activation_model import ActivationGraph, SealedActivationGraph
from neads.activation_model import SymbolicArgumentSet

import tests.my_test_utilities.arithmetic_plugins as ar_plugins


class TestExtractor(unittest.TestCase):
    def test_bad_number_of_inputs(self):
        ag = ActivationGraph(2)
        ag.add_activation(ar_plugins.const, ag.inputs[0])

        self.assertRaises(
            ValueError,
            Extractor,
            ag
        )

    def test_bad_number_of_result_activations(self):
        ag = ActivationGraph(3)
        ag.add_activation(ar_plugins.const, ag.inputs[0])
        ag.add_activation(ar_plugins.add, ag.inputs[0], 0)

        self.assertRaises(
            ValueError,
            Extractor,
            ag
        )

    def test_graph_has_graph_trigger(self):
        ag = ActivationGraph(3)
        ag.add_activation(ar_plugins.const, ag.inputs[0])
        ag.trigger_method = lambda: None

        self.assertRaises(
            ValueError,
            Extractor,
            ag
        )

    def test_graph_has_activation_trigger(self):
        ag = ActivationGraph(3)
        act = ag.add_activation(ar_plugins.const, ag.inputs[0])
        act.trigger_on_descendants = lambda: None

        self.assertRaises(
            ValueError,
            Extractor,
            ag
        )

    def test_attach(self):
        ag = ActivationGraph(3)
        ag.add_activation(ar_plugins.max,
                          ag.inputs[0], ag.inputs[1], ag.inputs[2])

        extractor = Extractor(ag)

        target_graph = SealedActivationGraph()
        act_0 = target_graph.add_activation(ar_plugins.const, 10)
        act_1 = target_graph.add_activation(ar_plugins.const, 15)

        result_act = extractor.attach(target_graph, act_0, act_1, 20)

        actual = result_act.argument_set
        expected = SymbolicArgumentSet(ar_plugins.max,
                                       act_0.symbol, act_1.symbol, 20)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
