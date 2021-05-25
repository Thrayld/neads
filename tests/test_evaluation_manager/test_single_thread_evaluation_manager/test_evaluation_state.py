import unittest

from typing import Any, Optional

from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_state import EvaluationState
from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
    import State, DataNodeStateException
from neads.database import Database, DataNotFound
from neads.activation_model import *

import tests._arithmetic_plugins as ar_plugins


MEMORY_LIMIT = 1_000_000_000


# TODO: Explore possibilities of testing memory handling
#  probably mock and something will be needed

def get_graph_1():
    ag = SealedActivationGraph()
    act_1 = ag.add_activation(ar_plugins.const, 1)
    act_2 = ag.add_activation(ar_plugins.add, act_1, 19)
    act_3 = ag.add_activation(ar_plugins.add, act_1, 9)
    act_4 = ag.add_activation(ar_plugins.sub, act_2, act_3)
    return ag, [act_1, act_2, act_3, act_4]


class TestEvaluationStateFailureCases(unittest.TestCase):
    """Test all bad uses of ES and DN."""

    def setUp(self) -> None:
        db = MockDatabase({})
        ag, acts = get_graph_1()
        self.es = EvaluationState(ag, db, MEMORY_LIMIT)

    def test_try_load_with_not_unknown(self):
        dn = self.es.get_top_level()[0]
        assert not dn.try_load()

        self.assertRaises(
            DataNodeStateException,
            dn.try_load
        )

    def test_evaluate_with_not_no_data(self):
        dn = self.es.get_top_level()[0]

        self.assertRaises(
            DataNodeStateException,
            dn.evaluate
        )

    def test_store_with_not_memory(self):
        dn = self.es.get_top_level()[0]

        self.assertRaises(
            DataNodeStateException,
            dn.store
        )

    def test_load_with_not_disk(self):
        dn = self.es.get_top_level()[0]

        self.assertRaises(
            DataNodeStateException,
            dn.load
        )

    def test_evaluate_with_parent_not_memory(self):
        dn = self.es.get_top_level()[0]
        assert not dn.try_load()
        dn.evaluate()
        dn.store()
        assert dn.state is State.DISK

        child = dn.children[0]
        assert not child.try_load()
        assert child.state is State.NO_DATA

        self.assertRaises(
            RuntimeError,
            child.evaluate
        )


class TestEvaluationStateBasicBehavior(unittest.TestCase):
    """Test basic behavior of ES and DN.

    There is AG without TMs and we test state of ES properties (without
    dynamic memory, see TODO above).
    Some calls of state changing methods are also performed in certain tests.

    We mainly test the DN's methods which launch some changes in ES and so on.
    Register methods are tested indirectly by examining reactions of ES to
    change of DN.
    """

    def test_memory_limit(self):
        self.assertEqual(True, False)

    def test_result_nodes(self):
        self.assertEqual(True, False)

    def test_dn_try_load_success(self):
        self.assertEqual(True, False)

    def test_dn_try_load_fail(self):
        self.assertEqual(True, False)

    def test_dn_evaluate(self):
        self.assertEqual(True, False)

    def test_dn_store(self):
        self.assertEqual(True, False)

    def test_dn_load(self):
        self.assertEqual(True, False)

    def test_evaluation_of_the_whole_graph(self):
        self.assertEqual(True, False)


class TestEvaluationStateWithTriggerMethods(unittest.TestCase):
    """Test behavior of ES and DN regarding a presence of trigger methods.

    In particular, we are interested in automatic invocation of TMs
    (on-result, on-descendants, graph's) and in consequent state of ES and DN
    (integration of new Activations to ES and their properties and behavior).

    For this purpose a few AGs is designed to stretch a particular feature
    of ES.
    """

    def test_invocation_tm_on_result(self):
        self.assertEqual(True, False)

    def test_invocation_tm_on_result_and_on_descendants(self):
        self.assertEqual(True, False)

    def test_cascade_invocation_tm_on_descendants(self):
        self.assertEqual(True, False)

    def test_graphs_tm_immediate_invocation(self):
        self.assertEqual(True, False)

    def test_cascade_invocation_on_result_on_descendants_graphs(self):
        self.assertEqual(True, False)


class EvaluationStateTester:
    pass


class MockDatabase(Database):
    def __init__(self, database_content: Optional[dict[DataDefinition, Any]]):
        if database_content is None:
            database_content = {}
        self._content = database_content

    # TODO: should open/close be also implemented?
    def open(self):
        pass

    def close(self):
        pass

    def save(self, data, data_definition):
        self._content[data_definition] = data

    def load(self, data_definition):
        try:
            return self._content[data_definition]
        except KeyError as e:
            raise DataNotFound() from e


if __name__ == '__main__':
    unittest.main()
