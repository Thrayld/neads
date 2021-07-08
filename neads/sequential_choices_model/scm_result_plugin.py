from typing import TYPE_CHECKING, Deque
import collections

from neads.plugin import Plugin, PluginID
from neads.sequential_choices_model.result_tree import ResultTree

if TYPE_CHECKING:
    from neads.sequential_choices_model.result_tree import ResultNode


def _plugin_method(structure_description):
    """Bring together data of all demanded levels put them in result structure.

    Parameters
    ----------
        Sequence which uniquely describes the ResultTree which is
        the result of SCM's evaluation (i.e. of the graph created by SCM).
        The list contain one entry for each node in the tree. The
        entries are in BFS order.
        Each entry consists of a dictionary, which contains the number of
        node's children (to determine the tree shape) under key
        'child_count'. For some nodes, the dictionary also contain key
        'data' with symbol of the appropriate Activation (i.e. the one
        that corresponds to the node in the TreeView).

    Returns
    -------
        Instance of ResultTree whose shape corresponds to the given
        `structure_description`.

    Raises
    ------
    ValueError
        If there is a mismatch between declared number of children and length
        of the description. That is, the sum of 'child_count' values is
        different from the length of the description - 1.
    """

    # Error checking
    child_sum = sum(node_desc['child_count']
                    for node_desc in structure_description)
    expected_sum = len(structure_description) - 1
    if child_sum != expected_sum:
        raise ValueError(
            f"Sum of declared number of children ({child_sum}) does not "
            f"match to the expected sum ({expected_sum}), i.e. the length of "
            f"the 'structure_description' - 1."
        )

    # Creation of the tree
    tree = ResultTree()
    queue: Deque[ResultNode] = collections.deque()
    queue.append(tree.root)
    # For all described nodes
    for node_desc in structure_description:
        current_node = queue.popleft()
        # Create children and add them to the queue (i.e. queue is BFS-ordered)
        child_count = node_desc['child_count']
        for idx in range(child_count):
            child = current_node.add_child()
            queue.append(child)
        # Assign data to the node, if there are any
        if 'data' in node_desc:
            current_node.data = node_desc['data']

    return tree


result_plugin = Plugin(PluginID('scm_result_plugin', 0), _plugin_method)
