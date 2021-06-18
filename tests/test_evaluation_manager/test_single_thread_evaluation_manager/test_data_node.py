import unittest

from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
    import DataNode, DataNodeStateException, DataNodeState
from neads.activation_model import *

import tests.my_test_utilities.arithmetic_plugins as ar_plugins
from tests.my_test_utilities.mock_database import MockDatabase


class TestDataNodeSingleNode(unittest.TestCase):

    def setUp(self) -> None:
        ag = SealedActivationGraph()
        db = MockDatabase({})

        self.act = ag.add_activation(ar_plugins.const, 10)
        self.dn = DataNode(self.act, [], db)

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
        pass

    def test_transition_unknown_to_memory(self):
        pass

    def test_transition_no_data_to_memory(self):
        pass

    def test_transition_memory_to_disk(self):
        pass

    def test_transition_disk_to_memory(self):
        pass

    def test_data_size(self):
        pass


class TestDataNodeInGraph(unittest.TestCase):

    def test_parents(self):
        pass

    def test_children(self):
        pass

    def test_level(self):
        pass

    def test_has_trigger_on_result(self):
        pass

    def test_has_trigger_on_descendants(self):
        pass

    # def test_evaluate_with_parent_not_memory(self):
    #     dn = self.es.get_top_level()[0]
    #     assert not dn.try_load()
    #     dn.evaluate()
    #     dn.store()
    #     assert dn.state is DataNodeState.DISK
    #
    #     child = dn.children[0]
    #     assert not child.try_load()
    #     assert child.state is DataNodeState.NO_DATA
    #
    #     self.assertRaises(
    #         RuntimeError,
    #         child.evaluate
    #     )


if __name__ == '__main__':
    unittest.main()
