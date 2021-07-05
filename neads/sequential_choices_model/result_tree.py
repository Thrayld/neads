from __future__ import annotations

from typing import Any, Union, Sequence, Optional


class ResultTree:
    """Tree whose nodes can carry data and they can be queried."""

    def __init__(self):
        """Initialize ResultTree."""

        raise NotImplementedError()

    @property
    def root(self) -> ResultNode:
        """The root of the tree."""
        raise NotImplementedError()

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

        raise NotImplementedError()


class ResultNode:
    _TOKEN = object()

    def __init__(self, /, _):
        """Initialize an instance of ResultNode.

        Parameters
        ----------
        _
            Token which guards the method from invoking from outside of the
            class.
        """

        raise NotImplementedError()
        # self.parent = parent
        # self.children = []

    @staticmethod
    def create_root() -> ResultNode:
        """Create a new root, i.e. a node without parent with name ()."""

        raise NotImplementedError()

    @property
    def name(self) -> tuple[int]:
        raise NotImplementedError()

    @property
    def has_data(self):
        """Whether any data was assigned to the node."""
        raise NotImplementedError()

    @property
    def data(self) -> Any:
        """Data of the node.

        Returns
        -------
            Data of the node or None if they are not assigned (or was deleted).
        """

        raise NotImplementedError()

    @data.setter
    def data(self, value):
        """Set the node's data."""
        raise NotImplementedError()

    @data.deleter
    def data(self):
        """Remove the node's data."""
        raise NotImplementedError()

    @property
    def parent(self) -> Optional[ResultNode]:
        """The parent of the node.

        Parent always exists except for the root.
        """
        raise NotImplementedError()

    @property
    def children(self) -> tuple[ResultNode]:
        """The children of the node."""
        raise NotImplementedError()

    def add_child(self) -> ResultNode:
        """Add new child to the node and return it.

        Returns
        -------
            The new created child whose name is the int tuple name of its
            parent with an extra last element which is index of the new node
            among its parent's children (starting from 0).
        """

        raise NotImplementedError()

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

        raise NotImplementedError()

    def __str__(self):
        """Return the name of the node."""
        raise NotImplementedError()
