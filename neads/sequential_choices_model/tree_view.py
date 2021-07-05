from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence
from frozendict import frozendict
import networkx as nx

from neads.sequential_choices_model.result_tree import ResultTree

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation


class TreeView:
    """Support structure which holds a tree view on an ActivationGraph.

    The point of SCM is to model and view the ActivationGraph as a global
    tree with vertices representing a small part of computation (Choice).

    The TreeView class contain only so-called result Activation of each Choice.
    """

    def __init__(self, root: SealedActivation):
        """Initialize TreeView with a root.

        Parameters
        ----------
        root
            Root node of the TreeView.
        """

        raise NotImplementedError()
        # self._tree_graph = nx.DiGraph()
        # self._tree_graph.add_node(root)
        # self._root = root

    def add_child(self, parent: SealedActivation, child: SealedActivation):
        """Add new child to the given parent.

        Parameters
        ----------
        parent
            Parent of the new child. The node must be already present in the
            TreeView.
        child
            The new child of the given parent. The node must not be present
            in the TreeView yet, as its re-addition would cause cycle in the
            graph.

        Raises
        ------
        ValueError
            If parent is not present in the graph.
            If the child is already present in the graph.
        """

        raise NotImplementedError()
        # if parent not in self._tree_graph:
        #     raise ValueError(
        #         f'The parent in not present in the graph: {parent}')
        # if child in self._tree_graph:
        #     raise ValueError(
        #         f'The child in already present in the graph: {child}')
        #
        # self._tree_graph.add_edge(parent, child)

    def create_result_description(self, levels_with_data: set[int]) \
            -> Sequence[frozendict]:
        """Create args list for the 'SCM result plugin' for ResultTree.

        The arguments are used by the plugin to create corresponding ResultTree.

        Parameters
        ----------
        levels_with_data
            Set of levels whose nodes are suppose to have their data in the
            ResultTree. The levels start with 0.

        Returns
        -------
            Return sequence which uniquely describes the ResultTree which is
            the result of SCM's evaluation (i.e. of the graph created by SCM).
            The sequence contain one entry for each node in the tree. The
            entries are in BFS order.
            Each entry consists of a frozendict, which contains the number of
            node's children (to determine the tree shape) under key
            'children_no'. For some nodes, the frozendict also contain key
            'data' with symbol of the appropriate Activation (i.e. the one
            that corresponds to the node in the TreeView).
        """

        raise NotImplementedError()
        # result_desc = []
        # current_level = [self._root]
        # no_current_level = 0
        # next_level = []
        # # While there are some on the current level
        # while current_level:
        #     # Process each node in current level
        #     for node in current_level:
        #         nodes_children = self._tree_graph.successors(node)
        #         children_no = len(nodes_children)
        #         if no_current_level in levels_with_data:
        #             node_description = frozendict(children_no=children_no,
        #                                           data=node.symbol)
        #         else:
        #             node_description = frozendict(children_no=children_no)
        #         result_desc.append(node_description)
        #         next_level.extend(nodes_children)
        #     # Prepare processing of the next level
        #     current_level = next_level
        #     no_current_level += 1
        #     next_level = []
        #
        # return result_desc

    # def draw(self):
    #     """Draw the captured tree structure."""
    #
    #     raise NotImplementedError()
