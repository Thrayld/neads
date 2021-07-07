import unittest
import unittest.mock as mock

from neads import ActivationGraph, DynamicStep, Extractor, Separator
from neads.activation_model import SealedActivationGraph

import tests.my_test_utilities.arithmetic_plugins as ar_plugins
from tests.my_test_utilities.assert_methods import assertEqualArgSets


def get_single_node_separator(plugin, /, *args, **kwargs):
    """Get separator with one node described by given arguments.

    But its first positional argument is the single graph's input!
    """

    ag = ActivationGraph(1)
    ag.add_activation(plugin, ag.inputs[0], *args, **kwargs)
    separator = Separator(ag)
    return separator


def get_single_node_extractor(plugin, /, *args, **kwargs):
    """Get choice with one node described by given arguments.

    But its first three positional arguments are the graph's inputs!
    """

    ag = ActivationGraph(3)
    ag.add_activation(plugin, ag.inputs[0], ag.inputs[1], ag.inputs[2],
                      *args, **kwargs)
    extractor = Extractor(ag)
    return extractor


class TestDynamicStep(unittest.TestCase):
    def setUp(self) -> None:
        self.target_graph = SealedActivationGraph()
        self.parent_act = self.target_graph.add_activation(ar_plugins.const, 6)
        self.tree_view_mock = mock.Mock()

        sep_a = get_single_node_separator(ar_plugins.factor)
        ext_a = get_single_node_extractor(ar_plugins.max)
        sep_b = get_single_node_separator(ar_plugins.factor)
        ext_b = get_single_node_extractor(ar_plugins.max)

        # Create ChoicesSteps
        ds_a = DynamicStep(sep_a, ext_a)
        ds_b = DynamicStep(sep_b, ext_b)

        ######
        # The test method invocation
        ds_a.create(self.target_graph, self.parent_act, self.tree_view_mock,
                    [ds_b])

    def test_dynamic_step_before_trigger_invocation(self):
        # Get created Activation
        act_sep_0, = self.parent_act.children

        # Test their ArgumentsSets
        assertEqualArgSets(act_sep_0, ar_plugins.factor, self.parent_act.symbol)

        # Assert calls to the TreeView object
        self.tree_view_mock.assert_not_called()

        # Test TM-on-result presence
        self.assertTrue(act_sep_0.trigger_on_result)

    def test_dynamic_step_after_trigger_invocation(self):
        # Get created Activation
        sep_a, = self.parent_act.children

        # Trigger invocation
        trigger = sep_a.trigger_on_result
        del sep_a.trigger_on_result
        trigger([2, 3])

        # Get created Activations
        ext_0, ext_1 = sep_a.children
        sep_0b, = ext_0.children
        sep_1b, = ext_1.children

        # Test their ArgumentsSets
        assertEqualArgSets(ext_0, ar_plugins.max, self.parent_act.symbol,
                           sep_a.symbol, 0)
        assertEqualArgSets(ext_1, ar_plugins.max, self.parent_act.symbol,
                           sep_a.symbol, 1)

        assertEqualArgSets(sep_0b, ar_plugins.factor, ext_0.symbol)
        assertEqualArgSets(sep_1b, ar_plugins.factor, ext_1.symbol)

        # Assert calls to the TreeView object
        expected = [
            (self.parent_act, ext_0),
            (self.parent_act, ext_1)
        ]
        actual = [args for args, _
                  in self.tree_view_mock.add_child.call_args_list]
        self.assertCountEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
