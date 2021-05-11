import unittest
from parameterized import parameterized

from neads.activation_model.activation_graph import ActivationGraph, \
    SealedActivationGraph, Activation
from neads.activation_model.symbolic_argument_set import SymbolicArgumentSet

import tests._arithmetic_plugins as ar_plugins


class TestActivationGraphFailureCases(unittest.TestCase):
    """Common test class for invalid operations."""

    def setUp(self) -> None:
        self.ag = ActivationGraph(2)
        self.other_ag = ActivationGraph(2)

        self.act = self.ag.add_activation(ar_plugins.add, 1, 2)
        self.foreign_act = self.other_ag.add_activation(ar_plugins.add, 1, 2)

        def trigger_result(act, result):  # noqa
            return []

        def trigger_descendants(act):  # noqa
            return []

        def trigger_graph(graph):  # noqa
            return []

        self.trigger_result = trigger_result
        self.trigger_descendants = trigger_descendants
        self.trigger_graph = trigger_graph

    @parameterized.expand([
        ('get_parents',),
        ('get_used_inputs',),
        ('get_children',),
        ('get_symbol',),
        ('get_plugin',),
        ('get_level',),
        ('get_argument_set',),
        ('get_trigger_on_result',),
        ('get_trigger_on_descendants',),
    ])
    def test_get_methods_foreign_activation(self, name):
        method = getattr(self.ag, name)
        foreign_act = ActivationGraph(1).add_activation(ar_plugins.add, 1, 2)

        self.assertRaises(
            ValueError,
            method,
            foreign_act
        )

    @parameterized.expand([
        ('remove_activation_trigger_on_result',),
        ('remove_activation_trigger_on_descendants',),
    ])
    def test_remove_non_present_activation_trigger(self, name):
        method = getattr(self.ag, name)

        self.assertRaises(
            RuntimeError,
            method,
            self.act
        )

    def test_remove_non_present_graph_trigger(self):
        self.assertRaises(
            RuntimeError,
            delattr,
            self.ag,
            'trigger_method'
        )

    def test_override_present_activation_trigger_on_result(self):
        self.act.trigger_on_result = self.trigger_result

        self.assertRaises(
            RuntimeError,
            self.ag.add_activation_trigger_on_result,
            self.act,
            self.trigger_result
        )

    def test_override_present_activation_trigger_on_descendants(self):
        self.act.trigger_on_descendants = self.trigger_descendants

        self.assertRaises(
            RuntimeError,
            self.ag.add_activation_trigger_on_descendants,
            self.act,
            self.trigger_descendants
        )

    def test_override_present_graph_trigger(self):
        self.ag.trigger_method = self.trigger_graph

        self.assertRaises(
            RuntimeError,
            setattr,
            self.ag,
            'trigger_method',
            self.trigger_graph
        )

    def test_add_activation_with_not_plugin(self):
        self.assertRaises(
            TypeError,
            self.ag.add_activation,
            lambda x, y: x+y,
            1,
            2
        )

    def test_add_activation_with_non_hashable_arg(self):
        self.assertRaises(
            TypeError,
            self.ag.add_activation,
            ar_plugins.add,
            1,
            ['non_hashable']
        )

    def test_add_activation_with_foreign_activation_symbol_in_arg(self):
        self.assertRaises(
            ValueError,
            self.ag.add_activation,
            ar_plugins.add,
            1,
            self.foreign_act.symbol
        )

    def test_add_activation_with_foreign_input_symbol_in_arg(self):
        self.assertRaises(
            ValueError,
            self.ag.add_activation,
            ar_plugins.add,
            1,
            self.other_ag.inputs[0]
        )

    def test_add_activation_with_improper_args_for_signature(self):
        self.assertRaises(
            TypeError,
            self.ag.add_activation,
            ar_plugins.add
        )

    def test_init_with_negative_inputs_count(self):
        self.assertRaises(
            ValueError,
            ActivationGraph,
            -1
        )


class TestActivationGraphExampleGraph(unittest.TestCase):
    """Test class for examining correct shape of an example graph."""

    @staticmethod
    def create_graph():
        ag = ActivationGraph(2)
        acts: list[Activation] = [None] * 4  # noqa

        acts[0] = ag.add_activation(ar_plugins.const, ag.inputs[0])
        acts[1] = ag.add_activation(ar_plugins.pow, acts[0].symbol)
        acts[2] = ag.add_activation(ar_plugins.add, acts[0].symbol,
                                    ag.inputs[1])
        acts[3] = ag.add_activation(ar_plugins.sub, acts[1].symbol,
                                    acts[2].symbol)

        return ag, acts

    def setUp(self) -> None:
        self.ag, self.acts = self.create_graph()

    @parameterized.expand([
        (0, []),
        (1, [0]),
        (2, [0]),
        (3, [1, 2]),
    ])
    def test_get_parents(self, idx, expected_indices):
        tested_act = self.acts[idx]
        expected_parents = [self.acts[idx] for idx in expected_indices]

        actual = tested_act.parents

        self.assertCountEqual(expected_parents, actual)

    @parameterized.expand([
        (0, [0]),
        (1, []),
        (2, [1]),
        (3, []),
    ])
    def test_get_used_inputs(self, idx, expected_indices):
        tested_act = self.acts[idx]
        expected_used_inputs = [self.ag.inputs[idx] for idx in expected_indices]

        actual = tested_act.used_inputs

        self.assertCountEqual(expected_used_inputs, actual)

    @parameterized.expand([
        (0, [1, 2]),
        (1, [3]),
        (2, [3]),
        (3, []),
    ])
    def test_get_children(self, idx, expected_indices):
        tested_act = self.acts[idx]
        expected_children = [self.acts[idx] for idx in expected_indices]

        actual = tested_act.children

        self.assertCountEqual(expected_children, actual)

    @parameterized.expand([
        (0, 'const'),
        (1, 'pow'),
        (2, 'add'),
        (3, 'sub'),
    ])
    def test_get_plugin(self, idx, plugin_name):
        tested_act = self.acts[idx]
        expected_plugin = getattr(ar_plugins, plugin_name)

        actual = tested_act.plugin

        self.assertEqual(expected_plugin, actual)

    @parameterized.expand([
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
    ])
    def test_get_level(self, idx, expected_level):
        tested_act = self.acts[idx]

        actual = tested_act.level

        self.assertEqual(expected_level, actual)

    def test_get_argument_sets(self):
        arg_sets = [
            SymbolicArgumentSet(ar_plugins.const.signature, self.ag.inputs[0]),
            SymbolicArgumentSet(ar_plugins.pow.signature, self.acts[0].symbol),
            SymbolicArgumentSet(ar_plugins.add.signature, self.acts[0].symbol,
                                self.ag.inputs[1]),
            SymbolicArgumentSet(ar_plugins.sub.signature, self.acts[1].symbol,
                                self.acts[2].symbol)
        ]

        for idx in range(4):
            expected = arg_sets[idx]
            actual = self.acts[idx].argument_set

            self.assertEqual(expected, actual)

    def test_iter(self):
        found_acts = list(self.ag)

        self.assertCountEqual(self.acts, found_acts)


class TestActivationGraphOtherMethods(unittest.TestCase):
    """Test class for other behavior not covered by previous two classes."""

    def setUp(self) -> None:
        self.ag = ActivationGraph(2)
        self.act = self.ag.add_activation(ar_plugins.add, 1, 2)

        def trigger_method(act, result):  # noqa
            return []

        self.trigger_method = trigger_method

    @parameterized.expand([
        ('trigger_on_result', 'act'),
        ('trigger_on_descendants', 'act'),
        ('trigger_method', 'graph'),
    ])
    def test_trigger_method_on_result_live_cycle(self, name, obj):
        if obj == 'act':
            tested_object = self.act
        else:
            tested_object = self.ag

        # Before assigment
        self.assertEqual(None, getattr(tested_object, name))

        # Assignment
        setattr(tested_object, name, self.trigger_method)

        # After assigment - trigger method present
        self.assertEqual(self.trigger_method, getattr(tested_object, name))

        # Delete
        delattr(tested_object, name)

        # After delete - None again
        self.assertEqual(None, getattr(tested_object, name))

    def test_add_existing_activation_due_default_value(self):
        act = self.ag.add_activation(ar_plugins.pow, 4)
        new_act = self.ag.add_activation(ar_plugins.pow, 4, 2)

        self.assertIs(act, new_act)

    def test_add_existing_activation_due_positional_vs_keyword_pass(self):
        new_act = self.ag.add_activation(ar_plugins.add, b=2, a=1)

        self.assertIs(self.act, new_act)


class TestSealedActivationGraph(unittest.TestCase):
    """Test class for special features of SAG opposed to AG."""

    def setUp(self) -> None:
        self.sag = SealedActivationGraph()
        self.other_sag = SealedActivationGraph()

        self.act = self.sag.add_activation(ar_plugins.add, 1, 2)
        self.foreign_act = self.other_sag.add_activation(ar_plugins.add, 1, 2)

    def test_get_definition_same_definitions(self):
        self.assertIsNot(self.act, self.foreign_act)
        self.assertIs(self.act.definition, self.foreign_act.definition)

    def test_get_definition_different_definitions(self):
        different_act = self.other_sag.add_activation(ar_plugins.sub, 1, 2)

        self.assertNotEqual(self.act.definition, different_act.definition)

    def test_get_definition_with_foreign_activation(self):
        self.assertRaises(
            ValueError,
            self.sag.get_definition,
            self.foreign_act
        )

    def test_inputs(self):
        self.assertEqual((), self.sag.inputs)

    def test_add_existing_activation_due_default_value(self):
        act = self.sag.add_activation(ar_plugins.pow, 4)
        new_act = self.sag.add_activation(ar_plugins.pow, 4, 2)

        self.assertIs(act, new_act)

    def test_add_existing_activation_due_positional_vs_keyword_pass(self):
        new_act = self.sag.add_activation(ar_plugins.add, b=2, a=1)

        self.assertIs(self.act, new_act)


if __name__ == '__main__':
    unittest.main()
