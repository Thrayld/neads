import unittest
import unittest.mock as mock

from typing import Any

from neads.activation_model import SealedActivationGraph
from neads.evaluation_manager.single_thread_evaluation_manager \
    .evaluation_state import EvaluationState

import tests.my_test_utilities.arithmetic_plugins as ar_plugins
from tests.my_test_utilities.mock_database import MockDatabase


def get_empty_trigger_mock():
    """Return Mock with empty list as a return_value."""
    trigger_mock = mock.Mock()
    trigger_mock.return_value = []
    return trigger_mock

class TestEvaluationStateMemoryMethods(unittest.TestCase):
    def setUp(self):
        mock_path = 'neads.evaluation_manager' \
                    '.single_thread_evaluation_manager' \
                    '.evaluation_state' \
                    '.memory_info'
        self.patcher = mock.patch(mock_path)
        self.memory_info_mock = self.patcher.start()

        self.vms = 1
        self.rss = 2
        self.av_mem = 3

        self.memory_info_mock.get_process_virtual_memory.return_value = self.vms
        self.memory_info_mock.get_process_ram_memory.return_value = self.rss
        self.memory_info_mock.get_available_memory.return_value = self.av_mem

        ag = SealedActivationGraph()
        ag.add_activation(ar_plugins.const, 10)

        self.es = EvaluationState(ag, MockDatabase())

    def tearDown(self):
        self.patcher.stop()

    def test_used_virtual_memory(self):
        self.assertEqual(self.vms, self.es.used_virtual_memory)

    def test_used_physical_memory(self):
        self.assertEqual(self.rss, self.es.used_physical_memory)

    def test_available_memory(self):
        self.assertEqual(self.av_mem, self.es.available_memory)


class ESExpected:
    def __init__(
            self,
            *,
            memory_nodes: Any = 'no_test',
            disk_nodes: Any = 'no_test',
            unknown_nodes: Any = 'no_test',
            no_data_nodes: Any = 'no_test',
            objectives: Any = 'no_test',
            results: Any = 'no_test',
            top_level: Any = 'no_test',
            has_graph_trigger: Any = 'no_test',
            it: Any = 'no_test'
    ):
        self.memory_nodes = memory_nodes
        self.disk_nodes = disk_nodes
        self.unknown_nodes = unknown_nodes
        self.no_data_nodes = no_data_nodes
        self.objectives = objectives
        self.results = results
        self.top_level = top_level
        self.has_graph_trigger = has_graph_trigger
        self.it = it


tc = unittest.TestCase()  # Enable access to assert methods to test method below
error_message = 'Difference in {}'


def assertEvaluationShapeIs(expected_values: ESExpected,  # noqa
                            actual_es: EvaluationState):
    for attribute, attr_value in expected_values.__dict__.items():
        message = error_message.format(attribute)
        if attr_value != 'no_test':
            if attribute in ['objectives', 'results', 'top_level'] \
                    or attribute.endswith('_nodes'):
                actual = getattr(actual_es, attribute)
                tc.assertCountEqual(attr_value, actual, message)
            elif attribute == 'has_graph_trigger':
                actual = getattr(actual_es, attribute)
                tc.assertEqual(attr_value, actual, message)
            elif attribute == 'it':
                actual = list(actual_es)
                tc.assertCountEqual(attr_value, actual, message)


class TestEvaluationStateSimpleStateChangesNoTriggers(unittest.TestCase):
    def setUp(self) -> None:
        ag = SealedActivationGraph()
        self.act = ag.add_activation(ar_plugins.const, 10)

        self.db = MockDatabase()
        self.es = EvaluationState(ag, self.db)

        assert len(self.es.top_level) == 1
        self.dn = next(iter(self.es))

        self.expected_state = ESExpected(
            memory_nodes=[],
            disk_nodes=[],
            unknown_nodes=[],
            no_data_nodes=[],
            objectives=[],
            results=[self.dn],
            top_level=[self.dn],
            has_graph_trigger=False,
            it=[self.dn]
        )

    def test_es_after_creation(self):
        self.expected_state.unknown_nodes = [self.dn]

        assertEvaluationShapeIs(self.expected_state, self.es)

    def test_simple_react_to_successful_try_load(self):
        self.db.save(10, self.act.definition)

        self.dn.try_load()

        self.expected_state.memory_nodes = [self.dn]
        assertEvaluationShapeIs(self.expected_state, self.es)

    def test_simple_react_to_unsuccessful_try_load(self):
        self.dn.try_load()

        self.expected_state.no_data_nodes = [self.dn]
        assertEvaluationShapeIs(self.expected_state, self.es)

    def test_simple_react_to_evaluate(self):
        self.dn.try_load()
        self.dn.evaluate()

        self.expected_state.memory_nodes = [self.dn]
        assertEvaluationShapeIs(self.expected_state, self.es)

    def test_simple_react_to_store(self):
        self.dn.try_load()
        self.dn.evaluate()
        self.dn.store()

        self.expected_state.disk_nodes = [self.dn]
        assertEvaluationShapeIs(self.expected_state, self.es)

    def test_simple_react_to_load(self):
        self.dn.try_load()
        self.dn.evaluate()
        self.dn.store()
        self.dn.load()

        self.expected_state.memory_nodes = [self.dn]
        assertEvaluationShapeIs(self.expected_state, self.es)


class TestEvaluationStateWithTriggersSimple(unittest.TestCase):
    """Tests cases with single node an a trigger called as soon as possible."""

    @staticmethod
    def get_expected_state_template(data_node):
        expected_state = ESExpected(
            memory_nodes=[],
            disk_nodes=[],
            unknown_nodes=[],
            no_data_nodes=[],
            objectives=[],
            results=[],
            top_level=[data_node],
            has_graph_trigger=False,
            it=[data_node]
        )
        return expected_state

    def setUp(self) -> None:
        self.ag = SealedActivationGraph()
        self.act = self.ag.add_activation(ar_plugins.const, 10)

        self.db = MockDatabase()
        # Cannot create ES right-away, first the triggers need be assigned

    def test_node_with_trigger_on_result(self):
        act_trigger = get_empty_trigger_mock()
        self.act.trigger_on_result = act_trigger
        es = EvaluationState(self.ag, self.db)
        dn = next(iter(es))

        # Check state after initialization
        expected = self.get_expected_state_template(dn)
        expected.unknown_nodes = [dn]
        expected.objectives = [dn]
        assertEvaluationShapeIs(expected, es)

        # Do the changes
        dn.try_load()
        dn.evaluate()

        # Check the changes on ES
        expected = self.get_expected_state_template(dn)
        expected.memory_nodes = [dn]
        expected.results = [dn]
        assertEvaluationShapeIs(expected, es)

        act_trigger.assert_called_once_with(10)  # Trigger was called
        self.assertIsNone(self.act.trigger_on_result)  # It is removed now

    def test_node_with_trigger_on_descendants(self):
        act_trigger = get_empty_trigger_mock()
        self.act.trigger_on_descendants = act_trigger
        es = EvaluationState(self.ag, self.db)
        dn = next(iter(es))

        # The trigger's are supposed to be called ASAP, thus, right after
        # ES's creation
        # No action is needed, we can immediately check the results
        expected = self.get_expected_state_template(dn)
        expected.unknown_nodes = [dn]
        expected.results = [dn]
        assertEvaluationShapeIs(expected, es)

        act_trigger.assert_called_once_with()  # Trigger was called
        self.assertIsNone(self.act.trigger_on_descendants)  # It is removed now

    def test_node_with_graph_trigger(self):
        graph_trigger = get_empty_trigger_mock()
        self.ag.trigger_method = graph_trigger
        es = EvaluationState(self.ag, self.db)
        dn = next(iter(es))

        # The trigger's are supposed to be called ASAP, thus, right after
        # ES's creation
        # No action is needed, we can immediately check the results
        expected = self.get_expected_state_template(dn)
        expected.unknown_nodes = [dn]
        expected.results = [dn]
        assertEvaluationShapeIs(expected, es)

        graph_trigger.assert_called_once_with()  # Trigger was called
        self.assertIsNone(self.ag.trigger_method)  # It is removed now


class TestEvaluationStateWithTriggersComplex(unittest.TestCase):
    def setUp(self) -> None:
        self.ag = SealedActivationGraph()
        self.db = MockDatabase()

    @staticmethod
    def get_expected_state_template():
        expected_state = ESExpected(
            memory_nodes=[],
            disk_nodes=[],
            unknown_nodes=[],
            no_data_nodes=[],
            objectives=[],
            results=[],
            top_level=[],
            has_graph_trigger=False,
            it=[]
        )
        return expected_state

    def test_trigger_cascade_result_descendants_graph(self):
        # Create graph
        graph_trigger = get_empty_trigger_mock()
        act_1_trigger = get_empty_trigger_mock()
        act_2_trigger = get_empty_trigger_mock()
        act_2_trigger.return_value = []

        act_1 = self.ag.add_activation(ar_plugins.const, 10)
        act_2 = self.ag.add_activation(ar_plugins.add, act_1.symbol, 15)

        self.ag.trigger_method = graph_trigger
        act_1.trigger_on_descendants = act_1_trigger
        act_2.trigger_on_result = act_2_trigger

        # Create ES and DNs
        es = EvaluationState(self.ag, self.db)
        dn_1 = next(iter(es.top_level))
        dn_2 = dn_1.children[0]

        # Check ES after init
        expected = self.get_expected_state_template()
        expected.unknown_nodes = [dn_1, dn_2]
        expected.objectives = [dn_2]
        expected.top_level = [dn_1]
        expected.has_graph_trigger = True
        expected.it = [dn_1, dn_2]
        assertEvaluationShapeIs(expected, es)

        # Launch the cascade
        self.db.save(25, act_2.definition)
        dn_2.try_load()

        # Check ES
        expected = self.get_expected_state_template()
        expected.unknown_nodes = [dn_1]
        expected.memory_nodes = [dn_2]
        expected.results = [dn_2]
        expected.top_level = [dn_1]
        expected.it = [dn_1, dn_2]
        assertEvaluationShapeIs(expected, es)

        # Check triggers
        graph_trigger.assert_called_once_with()
        self.assertIsNone(self.ag.trigger_method)

        act_1_trigger.assert_called_once_with()
        self.assertIsNone(act_1.trigger_on_descendants)

        act_2_trigger.assert_called_once_with(25)
        self.assertIsNone(act_2.trigger_on_result)

    def test_immediate_trigger_cascade_descendants_graph(self):
        # Create graph
        graph_trigger = get_empty_trigger_mock()
        descendants_trigger = get_empty_trigger_mock()

        act_1 = self.ag.add_activation(ar_plugins.const, 10)

        self.ag.trigger_method = graph_trigger
        act_1.trigger_on_descendants = descendants_trigger

        # Create ES and DNs
        es = EvaluationState(self.ag, self.db)
        dn_1 = next(iter(es.top_level))

        # Check ES after init which was supposed to launch the cascade
        expected = self.get_expected_state_template()
        expected.unknown_nodes = [dn_1]
        expected.results = [dn_1]
        expected.top_level = [dn_1]
        expected.it = [dn_1]
        assertEvaluationShapeIs(expected, es)

        # Check triggers
        graph_trigger.assert_called_once_with()
        self.assertIsNone(self.ag.trigger_method)

        descendants_trigger.assert_called_once_with()
        self.assertIsNone(act_1.trigger_on_descendants)

    def test_result_creates_node_with_descendants_immediately_called(self):
        # Create graph
        act_1 = self.ag.add_activation(ar_plugins.const, 10)
        act_2 = None
        act_2_trigger = get_empty_trigger_mock()
        # For easy check act_1_trigger invocation
        act_1_trigger_call_watch = mock.Mock()

        def act_1_trigger(_):
            nonlocal act_2
            act_1_trigger_call_watch()
            act_2 = self.ag.add_activation(ar_plugins.add, act_1.symbol, 15)
            act_2.trigger_on_descendants = act_2_trigger
            return [act_2]

        act_1.trigger_on_result = act_1_trigger

        # Create ES and DNs
        es = EvaluationState(self.ag, self.db)
        dn_1 = next(iter(es.top_level))

        # Check ES after creation
        expected = self.get_expected_state_template()
        expected.unknown_nodes = [dn_1]
        expected.objectives = [dn_1]
        expected.top_level = [dn_1]
        expected.it = [dn_1]
        assertEvaluationShapeIs(expected, es)

        # Launch the cascade
        dn_1.try_load()
        dn_1.evaluate()

        # Check ES
        dn_2 = dn_1.children[0]
        expected = self.get_expected_state_template()
        expected.unknown_nodes = [dn_2]
        expected.memory_nodes = [dn_1]
        expected.results = [dn_2]
        expected.top_level = [dn_1]
        expected.it = [dn_1, dn_2]
        assertEvaluationShapeIs(expected, es)

        # Check triggers
        act_1_trigger_call_watch.assert_called_once_with()
        self.assertIsNone(act_1.trigger_on_result)

        act_2_trigger.assert_called_once_with()
        self.assertIsNone(act_2.trigger_on_descendants)  # noqa

    def test_result_sets_descendants_trigger_on_itself(self):
        # Create graph
        act_1 = self.ag.add_activation(ar_plugins.const, 10)
        # For easy check act_1_trigger invocation
        act_1_trigger_call_watch = mock.Mock()
        act_1_trigger_on_descendants = get_empty_trigger_mock()

        def act_1_trigger_on_result(_):
            act_1_trigger_call_watch()
            act_1.trigger_on_descendants = act_1_trigger_on_descendants
            return []

        act_1.trigger_on_result = act_1_trigger_on_result

        # Create ES and DNs
        es = EvaluationState(self.ag, self.db)
        dn_1 = next(iter(es.top_level))

        # Check ES after creation
        expected = self.get_expected_state_template()
        expected.unknown_nodes = [dn_1]
        expected.objectives = [dn_1]
        expected.top_level = [dn_1]
        expected.it = [dn_1]
        assertEvaluationShapeIs(expected, es)

        # Launch the cascade
        dn_1.try_load()
        dn_1.evaluate()

        # Check ES
        expected = self.get_expected_state_template()
        expected.memory_nodes = [dn_1]
        expected.results = [dn_1]
        expected.top_level = [dn_1]
        expected.it = [dn_1]
        assertEvaluationShapeIs(expected, es)

        # Check triggers
        act_1_trigger_call_watch.assert_called_once_with()
        self.assertIsNone(act_1.trigger_on_result)

        act_1_trigger_on_descendants.assert_called_once_with()
        self.assertIsNone(act_1.trigger_on_descendants)


if __name__ == '__main__':
    unittest.main()
