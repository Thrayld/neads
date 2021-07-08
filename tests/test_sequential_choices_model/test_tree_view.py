import unittest

from neads.activation_model import SealedActivationGraph
from neads.sequential_choices_model.tree_view import TreeView

import tests.my_test_utilities.arithmetic_plugins as ar_plugins


class TestTreeView(unittest.TestCase):
    def test_add_child_already_present_child(self):
        ag = SealedActivationGraph()
        act_ = ag.add_activation(ar_plugins.const, 0)
        act_0 = ag.add_activation(ar_plugins.add, act_.symbol, 4)
        act_1 = ag.add_activation(ar_plugins.pow, act_.symbol)
        common_act = ag.add_activation(ar_plugins.add,
                                       act_0.symbol, act_1.symbol)

        tree_view = TreeView(act_)
        tree_view.add_child(act_, act_0)
        tree_view.add_child(act_, act_1)
        tree_view.add_child(act_0, common_act)

        self.assertRaises(
            ValueError,
            tree_view.add_child,
            act_1,
            common_act
        )

    def test_add_child_non_present_parent(self):
        ag = SealedActivationGraph()
        act_ = ag.add_activation(ar_plugins.const, 0)
        act_0 = ag.add_activation(ar_plugins.add, act_.symbol, 4)
        act_00 = ag.add_activation(ar_plugins.mul, act_0.symbol, 5)
        tree_view = TreeView(act_)

        self.assertRaises(
            ValueError,
            tree_view.add_child,
            act_0,
            act_00
        )


class TestTreeViewOnExampleGraph(unittest.TestCase):
    def get_result(self, *data_presence):
        """Create expected result structure by the description.

        Parameters
        ----------
        data_presence
            Whether data of the node on the respective index should be passed.

        Returns
        -------
            List of the dictionaries by the description.
        """

        assert len(data_presence) == len(self.bfs_order)
        result = []
        for data, c, act \
                in zip(data_presence, self.child_count, self.bfs_order):
            if data:
                entry = dict(child_count=c, data=act.symbol)
            else:
                entry = dict(child_count=c)
            result.append(entry)
        return result

    def setUp(self) -> None:
        self.ag = SealedActivationGraph()
        self.act_ = self.ag.add_activation(ar_plugins.const, 0)
        self.act_0 = self.ag.add_activation(ar_plugins.add, self.act_.symbol, 4)
        self.act_00 = self.ag.add_activation(ar_plugins.mul,
                                             self.act_0.symbol, 5)
        self.act_01 = self.ag.add_activation(ar_plugins.sub,
                                             self.act_0.symbol, 10)
        self.act_1 = self.ag.add_activation(ar_plugins.pow, self.act_.symbol)
        self.act_10 = self.ag.add_activation(ar_plugins.pow, self.act_1.symbol)

        self.tree_view = TreeView(self.act_)
        self.tree_view.add_child(self.act_, self.act_0)
        self.tree_view.add_child(self.act_0, self.act_00)
        self.tree_view.add_child(self.act_0, self.act_01)
        self.tree_view.add_child(self.act_, self.act_1)
        self.tree_view.add_child(self.act_1, self.act_10)

        self.bfs_order = [
            self.act_,
            self.act_0,
            self.act_1,
            self.act_00,
            self.act_01,
            self.act_10
        ]
        self.child_count = [
            2,
            2,
            1,
            0,
            0,
            0
        ]

    def test_create_result_description_level_0(self):
        actual = self.tree_view.get_result_description({0})
        expected = self.get_result(True, *([False]*5))
        self.assertEqual(expected, actual)

    def test_create_result_description_level_1(self):
        actual = self.tree_view.get_result_description({1})
        expected = self.get_result(False, True, True, *([False]*3))
        self.assertEqual(expected, actual)

    def test_create_result_description_level_2(self):
        actual = self.tree_view.get_result_description({2})
        expected = self.get_result(*([False]*3), *([True]*3))
        self.assertEqual(expected, actual)

    def test_create_result_description_all_levels(self):
        actual = self.tree_view.get_result_description({0, 1, 2})
        expected = self.get_result(*([True]*6))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
