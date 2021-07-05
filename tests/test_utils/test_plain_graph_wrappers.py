import abc
import unittest

from neads.utils.plain_graph_wrappers import Plain1RGraphWrapper, \
    Plain1In1RGraphWrapper, Plain3In1RGraphWrapper
from neads.activation_model import ActivationGraph, SealedActivationGraph

import tests.my_test_utilities.arithmetic_plugins as ar_plugins


class ExclusionWrapper:
    class TestPlain1RGraphWrapper(unittest.TestCase):

        @abc.abstractmethod
        def get_class(self) -> type(Plain1RGraphWrapper):
            pass

        def get_number_of_inputs(self):
            return self.get_class()._expected_inputs()

        def test_bad_number_of_result_activations(self):
            ag = ActivationGraph(self.get_number_of_inputs())
            ag.add_activation(ar_plugins.const, ag.inputs[0])
            ag.add_activation(ar_plugins.add, ag.inputs[0], 5)

            self.assertRaises(
                ValueError,
                self.get_class(),
                ag
            )

        def test_graph_has_graph_trigger(self):
            ag = ActivationGraph(self.get_number_of_inputs())
            ag.add_activation(ar_plugins.const, ag.inputs[0])
            ag.trigger_method = lambda: None

            self.assertRaises(
                ValueError,
                self.get_class(),
                ag
            )

        def test_graph_has_activation_trigger(self):
            ag = ActivationGraph(self.get_number_of_inputs())
            act = ag.add_activation(ar_plugins.const, ag.inputs[0])
            act.trigger_on_descendants = lambda: None

            self.assertRaises(
                ValueError,
                self.get_class(),
                ag
            )


class TestPlain1In1RGraphWrapper(ExclusionWrapper.
                                 TestPlain1RGraphWrapper):
    def get_class(self):
        return Plain1In1RGraphWrapper

    def test_bad_number_of_inputs(self):
        ag = ActivationGraph(2)
        ag.add_activation(ar_plugins.const, ag.inputs[0])

        self.assertRaises(
            ValueError,
            self.get_class(),
            ag
        )

    def test_attach(self):
        ag = ActivationGraph(1)
        ag.add_activation(ar_plugins.const, ag.inputs[0])

        wrapper = self.get_class()(ag)

        target_graph = SealedActivationGraph()
        act = target_graph.add_activation(ar_plugins.const, 10)

        result_act = wrapper.attach(target_graph, act)

        self.assertIs(act.children[0], result_act)


class TestPlain3In1RGraphWrapper(ExclusionWrapper.
                                 TestPlain1RGraphWrapper):
    def get_class(self):
        return Plain3In1RGraphWrapper

    def test_bad_number_of_inputs(self):
        ag = ActivationGraph(2)
        ag.add_activation(ar_plugins.const, ag.inputs[0])

        self.assertRaises(
            ValueError,
            self.get_class(),
            ag
        )


if __name__ == '__main__':
    unittest.main()
