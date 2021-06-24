import unittest
import unittest.mock as mock

from typing import Any

from neads.activation_model import SealedActivationGraph
from neads.evaluation_manager.single_thread_evaluation_manager \
    .evaluation_state import EvaluationState

import tests.my_test_utilities.arithmetic_plugins as ar_plugins
from tests.my_test_utilities.mock_database import MockDatabase


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
        self.memory_info_mock.get_available_memory = self.av_mem

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


def assertEvaluationShapeIs(expected_values: ESExpected,  # noqa
                            actual_es: EvaluationState):
    for attribute, attr_value in expected_values.__dict__.items():
        if attr_value != 'no_test':
            if attribute in ['objectives', 'results', 'top_level'] \
                    or attribute.endswith('_nodes'):
                actual = getattr(actual_es, attribute)
                tc.assertCountEqual(attr_value, actual)
            elif attribute == 'has_graph_trigger':
                actual = getattr(actual_es, attribute)
                tc.assertEqual(attr_value, actual)
            elif attribute == 'it':
                actual = list(actual_es)
                tc.assertCountEqual(attr_value, actual)


class TestEvaluationStateSimpleStateChangesNoTriggers(unittest.TestCase):
    def setUp(self) -> None:
        ag = SealedActivationGraph()
        self.act = ag.add_activation(ar_plugins.const, 10)

        self.db = MockDatabase()
        self.es = EvaluationState(ag, self.db)

        assert len(self.es.top_level) == 1
        self.dn = next(iter(self.es.top_level))

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
    pass


class TestEvaluationStateWithTriggersComplex(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
