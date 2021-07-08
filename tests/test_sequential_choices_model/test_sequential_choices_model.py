import unittest
import unittest.mock as mock

from neads import SequentialChoicesModel, ChoicesStep, Choice, \
    ActivationGraph, ListObject, DictObject, Value
from neads.sequential_choices_model.scm_root_plugin import root_plugin
from neads.sequential_choices_model.scm_result_plugin import result_plugin

from tests.my_test_utilities.assert_methods import assertArgSetsEqual
import tests.my_test_utilities.arithmetic_plugins as ar_plugins


class TestSequentialChoicesModelFailureCases(unittest.TestCase):
    def setUp(self) -> None:
        self.scm = SequentialChoicesModel()

    def test_create_graph_data_presence_with_invalid_indices(self):
        self.scm.steps.append(ChoicesStep())
        self.assertRaises(
            ValueError,
            self.scm.create_graph,
            [1]  # SCM have only one level, thus, only allowed index is 0
        )

    def test_create_graph_no_steps(self):
        self.assertRaises(
            RuntimeError,
            self.scm.create_graph
        )


class TestSequentialChoicesModelMocking(unittest.TestCase):
    def setUp(self) -> None:
        self.scm = SequentialChoicesModel()

        # TreeView mock
        self.patcher_tree_view = mock.patch(
            'neads.sequential_choices_model.sequential_choices_model.TreeView')
        mock_tree_view_class = self.patcher_tree_view.start()
        self.mock_tree_view_instance = mock.Mock()
        mock_tree_view_class.return_value = self.mock_tree_view_instance

        # Step mocks
        self.step_0 = mock.Mock()
        self.step_1 = mock.Mock()
        self.step_2 = mock.Mock()
        self.scm.steps.extend([self.step_0, self.step_1, self.step_2])

        # Unusually the tested method
        self.scm.create_graph()

    def tearDown(self) -> None:
        self.patcher_tree_view.stop()

    def test_create_assert_first_step_called(self):
        self.step_0.create.assert_called_once()

    def test_create_assert_shape_of_target_graph(self):
        target_graph, parent_act, _, _ = self.step_0.create.call_args.args

        # Has just one Activation, which is the parent_act
        actual_activations = [act for act in target_graph]
        self.assertEqual([parent_act], actual_activations)

        # Argument set of the Activation
        assertArgSetsEqual(parent_act, root_plugin)

    def test_create_assert_the_used_tree_view(self):
        _, _, tree_view, _ = self.step_0.create.call_args.args
        # It should be the mock I assigned there
        self.assertIs(self.mock_tree_view_instance, tree_view)

    def test_create_graph_assert_the_next_steps(
            self):
        _, _, _, next_steps = self.step_0.create.call_args.args

        expected = [self.step_1, self.step_2]
        self.assertEqual(expected, next_steps)


def get_single_node_choice(plugin, /, *args, **kwargs):
    """Get choice with one node described by given arguments.

    But its first positional argument is the single graph's input!
    """

    ag = ActivationGraph(1)
    ag.add_activation(plugin, ag.inputs[0], *args, **kwargs)
    choice = Choice(ag)
    return choice


class TestSequentialChoicesModelWithRealClasses(unittest.TestCase):
    def setUp(self) -> None:
        self.scm = SequentialChoicesModel()

        # Step A
        step_a = ChoicesStep()
        choice_a = get_single_node_choice(ar_plugins.const)
        step_a.choices.append(choice_a)

        # Step B
        step_b = ChoicesStep()
        choice_b0 = get_single_node_choice(ar_plugins.add, 0)
        choice_b1 = get_single_node_choice(ar_plugins.mul, 2)
        step_b.choices.extend([choice_b0, choice_b1])

        self.scm.steps.extend([step_a, step_b])

    def test_create_graph_shape_right_after(self):
        scm_graph = self.scm.create_graph()

        # Assert the graph has only 4 Activations
        self.assertEqual(4, len(list(scm_graph)))

        # 'Parse' the Activations
        act_0, = scm_graph.get_top_level()
        act_00, = act_0.children
        act_000, act_001 = act_00.children

        # Check their argument sets
        assertArgSetsEqual(act_0, root_plugin)
        assertArgSetsEqual(act_00, ar_plugins.const, act_0.symbol)
        assertArgSetsEqual(act_000, ar_plugins.add, act_00.symbol, 0)
        assertArgSetsEqual(act_001, ar_plugins.mul, act_00.symbol, 2)

    def test_create_graph_shape_after_trigger_invocation(self):
        scm_graph = self.scm.create_graph()

        # Invoke the graph's trigger
        trigger = scm_graph.trigger_method
        del scm_graph.trigger_method
        trigger()

        # Assert the graph has only 5 Activations (addition of the result act)
        self.assertEqual(5, len(list(scm_graph)))

        # 'Parse' the Activations
        act_0, = scm_graph.get_top_level()
        act_00, = act_0.children
        act_000, act_001, result_act = act_00.children

        # Check argument set of the result Activation
        expected_argument = ListObject(
            DictObject({Value('child_count'): Value(1)}),
            DictObject({Value('child_count'): Value(2),
                        Value('data'): act_00.symbol}),
            DictObject({Value('child_count'): Value(0),
                        Value('data'): act_000.symbol}),
            DictObject({Value('child_count'): Value(0),
                        Value('data'): act_001.symbol}),
        )
        assertArgSetsEqual(result_act, result_plugin, expected_argument)


if __name__ == '__main__':
    unittest.main()
