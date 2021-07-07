import unittest
import unittest.mock as mock

from neads import ActivationGraph, Choice, ChoicesStep
from neads.activation_model import SealedActivationGraph

import tests.my_test_utilities.arithmetic_plugins as ar_plugins
from tests.my_test_utilities.assert_methods import assertEqualArgSets


def get_single_node_choice(plugin, /, *args, **kwargs):
    """Get choice with one node described by given arguments.

    But its first positional argument is the single graph's input!
    """

    ag = ActivationGraph(1)
    ag.add_activation(plugin, ag.inputs[0], *args, **kwargs)
    choice = Choice(ag)
    return choice


class TestChoicesStep(unittest.TestCase):
    def setUp(self) -> None:
        self.target_graph = SealedActivationGraph()
        self.parent_act = self.target_graph.add_activation(ar_plugins.const, 0)
        self.tree_view_mock = mock.Mock()
        self.add_child_mock = mock.Mock()
        self.tree_view_mock.add_child = self.add_child_mock

    def test_choices_step_create_with_next_step(self):
        # Create Choices
        c_a0 = get_single_node_choice(ar_plugins.const)
        c_a1 = get_single_node_choice(ar_plugins.add, 10)
        c_b0 = get_single_node_choice(ar_plugins.sub, 20)
        c_b1 = get_single_node_choice(ar_plugins.mul, 2)

        # Create ChoicesSteps
        cs_a = ChoicesStep()
        cs_a.choices = [c_a0, c_a1]

        cs_b = ChoicesStep()
        cs_b.choices = [c_b0, c_b1]

        ######
        # The test method invocation
        cs_a.create(self.target_graph, self.parent_act, self.tree_view_mock,
                    [cs_b])

        # Get created Activations
        act_0, act_1 = self.parent_act.children
        act_00, act_01 = act_0.children
        act_10, act_11 = act_1.children

        # Test their ArgumentsSets
        assertEqualArgSets(act_0, ar_plugins.const, self.parent_act.symbol)
        assertEqualArgSets(act_1, ar_plugins.add, self.parent_act.symbol, 10)

        assertEqualArgSets(act_00, ar_plugins.sub, act_0.symbol, 20)
        assertEqualArgSets(act_01, ar_plugins.mul, act_0.symbol, 2)

        assertEqualArgSets(act_10, ar_plugins.sub, act_1.symbol, 20)
        assertEqualArgSets(act_11, ar_plugins.mul, act_1.symbol, 2)

        # Assert calls to the TreeView object
        expected = [
            (self.parent_act, act_0),
            (self.parent_act, act_1),
            (act_0, act_00),
            (act_0, act_01),
            (act_1, act_10),
            (act_1, act_11)
        ]
        actual = [args for args, _ in self.add_child_mock.call_args_list]
        self.assertCountEqual(expected, actual)
        # self.add_child_mock.assert_called_with(self.parent_act, act_0)
        # self.add_child_mock.assert_called_with(self.parent_act, act_1)
        #
        # self.add_child_mock.assert_called_with(act_0, act_00)
        # self.add_child_mock.assert_called_with(act_0, act_01)
        #
        # self.add_child_mock.assert_called_with(act_1, act_10)
        # self.add_child_mock.assert_called_with(act_1, act_11)


if __name__ == '__main__':
    unittest.main()
