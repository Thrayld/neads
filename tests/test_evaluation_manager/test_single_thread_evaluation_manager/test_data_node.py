import unittest
import unittest.mock as mock

import pympler.asizeof
from parameterized import parameterized

from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
    import DataNode, DataNodeStateException, DataNodeState
from neads.activation_model import *

import tests.my_test_utilities.arithmetic_plugins as ar_plugins
from tests.my_test_utilities.mock_database import MockDatabase


class TestDataNodeSingleNode(unittest.TestCase):

    def setUp(self) -> None:
        ag = SealedActivationGraph()
        self.value = 10
        self.act = ag.add_activation(ar_plugins.const, self.value)

        self.db = MockDatabase()
        self.db.open()
        self.dn = DataNode(self.act, [], self.db)

        self.callback_mock = mock.Mock()

    def tearDown(self) -> None:
        self.db.close()

    def test_try_load_with_not_unknown(self):
        assert not self.dn.try_load()

        self.assertRaises(
            DataNodeStateException,
            self.dn.try_load
        )

    def test_evaluate_with_not_no_data(self):
        self.assertRaises(
            DataNodeStateException,
            self.dn.evaluate
        )

    def test_store_with_not_memory(self):
        self.assertRaises(
            DataNodeStateException,
            self.dn.store
        )

    def test_load_with_not_disk(self):
        self.assertRaises(
            DataNodeStateException,
            self.dn.load
        )

    def test_transition_unknown_to_no_data(self):
        self.dn.register_callback_unknown_to_no_data(self.callback_mock)

        assert not self.dn.try_load()

        self.callback_mock.assert_called()
        self.assertEqual(DataNodeState.NO_DATA, self.dn.state)

    def test_transition_unknown_to_memory(self):
        self.dn.register_callback_unknown_to_memory(self.callback_mock)
        self.db.save(self.value, self.act.definition)

        assert self.dn.try_load()

        self.callback_mock.assert_called()
        self.assertEqual(DataNodeState.MEMORY, self.dn.state)

    def test_transition_no_data_to_memory(self):
        self.dn.register_callback_no_data_to_memory(self.callback_mock)
        assert not self.dn.try_load()

        self.dn.evaluate()

        self.callback_mock.assert_called()
        self.assertEqual(DataNodeState.MEMORY, self.dn.state)

    def test_transition_memory_to_disk(self):
        self.dn.register_callback_memory_to_disk(self.callback_mock)
        assert not self.dn.try_load()
        self.dn.evaluate()

        self.dn.store()

        self.callback_mock.assert_called()
        self.assertEqual(DataNodeState.DISK, self.dn.state)

    def test_transition_disk_to_memory(self):
        self.dn.register_callback_disk_to_memory(self.callback_mock)
        assert not self.dn.try_load()
        self.dn.evaluate()
        self.dn.store()

        self.dn.load()

        self.callback_mock.assert_called()
        self.assertEqual(DataNodeState.MEMORY, self.dn.state)

    def test_different_callback_not_called(self):
        self.dn.register_callback_unknown_to_memory(self.callback_mock)

        assert not self.dn.try_load()

        self.callback_mock.assert_not_called()

    def test_data_size_before_having_data(self):
        self.assertEqual(None, self.dn.data_size)

    def test_data_size_with_data(self):
        self.dn.try_load()
        self.dn.evaluate()

        expected_size = pympler.asizeof.asizeof(self.value)
        self.assertEqual(expected_size, self.dn.data_size)


class TestDataNodeInGraph(unittest.TestCase):

    @staticmethod
    def _get_activation_graph():
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 0)
        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 20)
        act_3 = ag.add_activation(ar_plugins.add, act_1.symbol, 10)
        act_4 = ag.add_activation(ar_plugins.sub, act_2.symbol, act_3.symbol)

        act_1.trigger_on_descendants = mock.Mock()
        act_4.trigger_on_result = mock.Mock()
        return ag, [act_1, act_2, act_3, act_4]

    @staticmethod
    def _get_data_node_graph(ag, db):
        act_to_dn = {}
        dn_to_act = {}
        for act in sorted(ag, key=lambda act: act.level):
            parents = [act_to_dn[p] for p in act.parents]
            new_dn = DataNode(act, parents, db)
            act_to_dn[act] = new_dn
            dn_to_act[new_dn] = act
        return act_to_dn, dn_to_act

    def setUp(self) -> None:
        self.ag, self.acts = self._get_activation_graph()
        self.db = MockDatabase()
        self.db.open()
        self.act_to_dn, self.dn_to_act \
            = self._get_data_node_graph(self.ag, self.db)
        self.dns = [self.act_to_dn[act] for act in self.acts]

    def tearDown(self) -> None:
        self.db.close()

    @parameterized.expand([
        (0, []),
        (1, [0]),
        (2, [0]),
        (3, [1, 2]),
    ])
    def test_parents(self, node_idx, expected_parents_idxs):
        dn = self.dns[node_idx]

        actual_parent_idxs = [self.acts.index(self.dn_to_act[parent])
                              for parent in dn.parents]

        self.assertEqual(expected_parents_idxs, actual_parent_idxs)

    @parameterized.expand([
        (0, [1, 2]),
        (1, [3]),
        (2, [3]),
        (3, []),
    ])
    def test_children(self, node_idx, expected_children_idxs):
        dn = self.dns[node_idx]

        actual_children_idxs = [self.acts.index(self.dn_to_act[child])
                                for child in dn.children]

        self.assertEqual(expected_children_idxs, actual_children_idxs)

    @parameterized.expand([
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
    ])
    def test_level(self, node_idx, expected_level):
        dn = self.dns[node_idx]

        actual_level = dn.level

        self.assertEqual(expected_level, actual_level)

    @parameterized.expand([
        (0, False),
        (1, False),
        (2, False),
        (3, True),
    ])
    def test_has_trigger_on_result(self, node_idx, expected_value):
        dn = self.dns[node_idx]

        actual_value = dn.has_trigger_on_result

        self.assertEqual(expected_value, actual_value)

    @parameterized.expand([
        (0, True),
        (1, False),
        (2, False),
        (3, False),
    ])
    def test_has_trigger_on_descendants(self, node_idx, expected_value):
        dn = self.act_to_dn[self.acts[node_idx]]

        actual_value = dn.has_trigger_on_descendants

        self.assertEqual(expected_value, actual_value)

    def test_evaluate_with_parents(self):
        parent = self.dns[0]
        child = self.dns[1]

        parent.try_load()
        parent.evaluate()
        child.try_load()

        child.evaluate()

        self.assertEqual(DataNodeState.MEMORY, child.state)

    def test_evaluate_with_parents_not_in_memory(self):
        parent = self.dns[0]
        child = self.dns[1]

        parent.try_load()
        parent.evaluate()
        parent.store()
        assert parent.state is DataNodeState.DISK

        child.try_load()
        assert child.state is DataNodeState.NO_DATA

        # The actual test
        self.assertRaises(
            RuntimeError,
            child.evaluate
        )


if __name__ == '__main__':
    unittest.main()
