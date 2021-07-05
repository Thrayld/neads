import unittest

from neads.sequential_choices_model.result_tree import ResultNode, ResultTree


class TestResultNode(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ResultNode.create_root()

    def test_create_root(self):
        self.assertEqual((), self.root.name)
        self.assertEqual(None, self.root.parent)
        self.assertEqual((), self.root.children)

    def test_add_child(self):
        child_0 = self.root.add_child()
        child_00 = child_0.add_child()
        child_01 = child_0.add_child()
        child_1 = self.root.add_child()
        child_2 = self.root.add_child()

        self.assertEqual((0,), child_0.name)
        self.assertEqual((0, 0), child_00.name)
        self.assertEqual((0, 1), child_01.name)
        self.assertEqual((1,), child_1.name)
        self.assertEqual((2,), child_2.name)

    def test_work_with_data(self):
        # Before assignment
        self.assertEqual(None, self.root.data)
        self.assertEqual(False, self.root.has_data)

        self.root.data = 10

        # After assignment
        self.assertEqual(10, self.root.data)
        self.assertEqual(True, self.root.has_data)

        del self.root.data

        # After removal
        self.assertEqual(None, self.root.data)
        self.assertEqual(False, self.root.has_data)


class TestResultNodeSmallTree(unittest.TestCase):
    def setUp(self) -> None:
        # Tree with a few nodes, data have only the nodes in level 2 (with
        # name of length 2)
        self.root = ResultNode.create_root()

        self.child_0 = self.root.add_child()
        self.child_00 = self.child_0.add_child()
        self.child_00.data = '00'
        self.child_01 = self.child_0.add_child()
        self.child_01.data = '01'

        self.child_1 = self.root.add_child()
        self.child_10 = self.child_1.add_child()
        self.child_10.data = '10'

        self.child_2 = self.root.add_child()

    def test_query_without_wildcard(self):
        actual = self.root.query((0, 1))
        expected = [self.child_01]

        self.assertEqual(expected, actual)

    def test_query_with_wildcard(self):
        actual = self.root.query((0, None))
        expected = [self.child_00, self.child_01]

        self.assertEqual(expected, actual)

    def test_query_two_wildcards(self):
        actual = self.root.query((None, None))
        expected = [self.child_00, self.child_01, self.child_10]

        self.assertEqual(expected, actual)

    def test_query_on_non_root(self):
        actual = self.child_1.query((1,))
        expected = [self.child_1]

        self.assertEqual(expected, actual)

    def test_query_with_data(self):
        actual = self.root.query((0, None), data=True)
        expected = ['00', '01']

        self.assertEqual(expected, actual)

    def test_query_with_data_on_node_with_no_data(self):
        self.assertRaises(
            ValueError,
            self.root.query,
            (1,),
            data=True
        )


class TestResultTree(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = ResultTree()
        self.root = self.tree.root

        self.child_0 = self.root.add_child()
        self.child_00 = self.child_0.add_child()
        self.child_00.data = '00'

        self.child_1 = self.root.add_child()
        self.child_10 = self.child_1.add_child()
        self.child_10.data = '10'

        self.child_2 = self.root.add_child()

    def test_query_without_data(self):
        actual = self.tree.query((0, None))
        expected = [self.child_00]

        self.assertEqual(expected, actual)

    def test_query_with_data(self):
        actual = self.tree.query((0, None), data=True)
        expected = ['00']

        self.assertEqual(expected, actual)

    def test_query_with_data_on_node_with_no_data(self):
        self.assertRaises(
            ValueError,
            self.tree.query,
            (1,),
            data=True
        )


if __name__ == '__main__':
    unittest.main()
