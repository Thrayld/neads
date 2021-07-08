import unittest

from neads.sequential_choices_model.scm_result_plugin import _plugin_method
from neads.sequential_choices_model.result_tree import ResultTree

from tests.my_test_utilities.assert_methods import assertResultTreeEqual


def get_description(nodes_child_count, nodes_data):
    """Create description by the arguments.

    Parameters
    ----------
    nodes_child_count
        Sequence of ints.
    nodes_data
        Sequence of anything. Ellipsis is considered to be entry for 'no data'.

    Returns
    -------
        List of dictionaries of length corresponding to the length of
        `nodes_child_count` (and `nodes_data`). Each has key 'child_count'
        with corresponding int from `nodes_child_count`, some also contain
        key 'data' with the corresponding value in `nodes_data` if it is not
        Ellipsis (in that case, the key 'data' is missing).
    """
    assert len(nodes_child_count) == len(nodes_data)

    description = []
    # For all described nodes
    for cnt, data in zip(nodes_child_count, nodes_data):
        node_desc = {'child_count': cnt}
        if data is not Ellipsis:
            node_desc['data'] = data
        description.append(node_desc)
    return description


class TestSCMResultPlugin(unittest.TestCase):
    def test_call_wrong_number_of_entries_and_children(self):
        # Data for description
        child_count = [
            1,
            0,
            2,
            0,
            0
        ]
        data = [
            ...,
            None,
            None,
            'a',
            'b'
        ]
        description = get_description(child_count, data)

        self.assertRaises(
            ValueError,
            _plugin_method,
            description
        )

    def test_call_with_tree_1(self):
        # Data for description
        child_count = [
            2,
            0,
            2,
            0,
            0
        ]
        data = [
            ...,
            None,
            None,
            'a',
            'b'
        ]

        # Expected tree
        expected = ResultTree()
        root = expected.root
        # Creating nodes
        child_0 = root.add_child()
        child_1 = root.add_child()
        child_2 = child_1.add_child()
        child_3 = child_1.add_child()
        # Assigning data
        child_0.data = None
        child_1.data = None
        child_2.data = 'a'
        child_3.data = 'b'

        self.do_general_test(child_count, data, expected)

    def test_call_with_tree_2(self):
        # Data for description
        child_count = [
            2,
            2,
            0,
            0,
            0
        ]
        data = [
            None,
            0,
            1,
            ...,
            ...
        ]

        # Expected tree
        expected = ResultTree()
        root = expected.root
        # Creating nodes
        child_0 = root.add_child()
        child_1 = root.add_child()
        _ = child_0.add_child()
        _ = child_0.add_child()
        # Assigning data
        root.data = None
        child_0.data = 0
        child_1.data = 1

        self.do_general_test(child_count, data, expected)

    @staticmethod
    def do_general_test(child_count, data, expected_tree):
        description = get_description(child_count, data)

        # Invoke the tested method
        actual_tree = _plugin_method(description)

        assertResultTreeEqual(expected_tree, actual_tree)


if __name__ == '__main__':
    unittest.main()
