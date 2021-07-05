from __future__ import annotations

import itertools
from typing import Any, Union, Sequence, Optional


class ResultTree:
    """Tree whose nodes can carry data and they can be queried."""

    def __init__(self):
        """Initialize ResultTree."""

        self._root = ResultNode.create_root()

    @property
    def root(self) -> ResultNode:
        """The root of the tree."""
        return self._root

    def query(self, query: Sequence[Union[int, None]],
              *, data=False):
        """Return all nodes (or their data) which suits the query.

        The decision for each node (whether it suits the query) goes as
        follows. If the query has different length than the node's
        name, the node is not included.
        Otherwise, when the query is as long as the node's name, we compare
        the the query and the node's name entry by entry.
        If there is an index on which the sequence has an integer which
        differs from name's one (name is sequence of integers), the node is not
        included.
        That is, each integer in the query masks out all node's with
        different integer on the index. On the other hand, the None works
        as wildcard, i.e. with the meaning 'no restriction'.

        Parameters
        ----------
        query
            A sequence of integers and Nones which selects the result.
            A node (or its data) is included in the result, if its name suits
            the query.
        data
            Whether return nodes' data directly instead of the nodes.

        Returns
        -------
            List all nodes (or their data) which suits the query.
            The list is in BFS order from left to right.

        Raises
        ------
        ValueError
            If `data` is True and the query suits a node that does not have
            data.
        """

        return self.root.query(query, data=data)


class ResultNode:
    _TOKEN = object()

    def __init__(self, _, /, name: tuple[int], parent: Optional[ResultNode]):
        """Initialize an instance of ResultNode.

        Parameters
        ----------
        _
            Token which guards the method from invoking from outside of the
            class.
        name
            Name of the new node.
        parent
            Node's parent
        """

        self._name = name
        self._parent = parent
        self._children: list[ResultNode] = []

        self._has_data = False
        self._data = None

    @staticmethod
    def create_root() -> ResultNode:
        """Create a new root, i.e. a node without parent with name ()."""
        root = ResultNode(ResultNode._TOKEN, (), None)  # noqa
        return root

    @property
    def name(self) -> tuple[int]:
        return self._name

    @property
    def level(self) -> int:
        return len(self._name)

    @property
    def has_data(self):
        """Whether any data was assigned to the node."""
        return self._has_data

    @property
    def data(self) -> Any:
        """Data of the node.

        Returns
        -------
            Data of the node or None if they are not assigned (or was deleted).
        """

        return self._data

    @data.setter
    def data(self, value):
        """Set the node's data."""
        self._data = value
        self._has_data = True

    @data.deleter
    def data(self):
        """Remove the node's data."""
        self._data = None
        self._has_data = False

    @property
    def parent(self) -> Optional[ResultNode]:
        """The parent of the node.

        Parent always exists except for the root.
        """
        return self._parent

    @property
    def children(self) -> tuple[ResultNode]:
        """The children of the node."""
        return tuple(self._children)

    def add_child(self) -> ResultNode:
        """Add new child to the node and return it.

        Returns
        -------
            The new created child whose name is the int tuple name of its
            parent with an extra last element which is index of the new node
            among its parent's children (starting from 0).
        """

        child_index = len(self._children)
        child_name = tuple(itertools.chain(self._name, (child_index,)))
        child = ResultNode(self._TOKEN, child_name, self)  # noqa
        self._children.append(child)
        return child

    def query(self, query, *, data=False):
        """Return nodes in the subtree (or their data) which suits the query.

        The subtree is traversed using DFS to find all nodes which suits the
        query.

        See the description of the decision algorithm in `ResultTree.query`
        method.

        Parameters
        ----------
        query
            A sequence of integers and Nones which selects the result.
            A node (or its data) is included in the result, if its name suits
            the query.
        data
            Whether return nodes' data directly instead of the nodes.

        Returns
        -------
            List all nodes (or their data) which suits the query.
            The list is in BFS order from left to right.

        Raises
        ------
        ValueError
            If `data` is True and the query suits a node that does not have
            data.
        """

        return self._do_query(query, [], data)

    def _do_query(self, query, partial_results, data):
        """Does the query.

        Parameters
        ----------
        query
            The query, i.e. sequence of integers and Nones.
        partial_results
            List with a partial results.
        data
            Whether return nodes' data directly instead of the nodes.

        Returns
        -------
            The updates list with the partial results by nodes in the subtree
            whose root the `self` node.
        """

        # Process self
        if self._suits_query(query):
            if data:
                if self.has_data:
                    partial_results.append(self.data)
                else:
                    raise ValueError(f'The node {self} does not have data.')
            else:
                partial_results.append(self)

        # Process children
        if len(query) > len(self._name):
            for child in self._children:
                child._do_query(query, partial_results, data)

        return partial_results

    def _suits_query(self, query):
        """Return whether the node suits the query.

        See the description of the decision algorithm in `ResultTree.query`
        method.

        Parameters
        ----------
        query
            The query, i.e. sequence of integers and Nones.

        Returns
        -------
            True, if does, False otherwise.
        """

        if len(query) == len(self._name):
            for query_el, name_el in zip(query, self._name):
                if query_el is not None and query_el != name_el:
                    # Mismatch found
                    return False
            else:
                # Everything Ok
                return True
        else:
            # Different length
            return False

    def __str__(self):
        """Return the name of the node as string."""
        return str(self.name)
