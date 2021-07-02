from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Iterator, Sequence
import collections
import itertools

from neads.evaluation_manager.single_thread_evaluation_manager \
    .evaluation_algorithms.i_evaluation_algorithm import IEvaluationAlgorithm
from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
    import DataNodeState

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation
    from neads.evaluation_manager.single_thread_evaluation_manager \
        .evaluation_state import EvaluationState
    from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
        import DataNode


class ComplexAlgorithm(IEvaluationAlgorithm):
    """The algorithm which uses all EvaluationState capabilities.

    Most notably, it manages the memory consumption of the process and takes
    advantage of ES's database.

    The algorithm process the significant (objectives and results) nodes one
    by one. By DFS from the node to evaluate, its descendants are subsequently
    loaded or evaluated. Throughout the evaluation, the amount of consumed
    virtual memory is checked and kept around or below the memory limit by
    storing data of some nodes to disk.
    """

    def __init__(self, memory_limit):
        """Initialize the ComplexAlgorithm.

        Parameters
        ----------
        memory_limit
            Soft limit of virtual memory for the process. The consumption of
            virtual memory should not greatly exceed the limit.
        """

        # Soft limit of virtual memory for the process
        self._memory_limit = memory_limit

        self._evaluation_state: Optional[EvaluationState] = None

        # Order in which the nodes are stored to disk (from start)
        self._swap_order = collections.deque()

        # State of processing the current node
        self._necessary = []  # Nodes whose data are guaranteed to be used
        self._visited = []  # Visited and processed nodes

    def evaluate(self, evaluation_state: EvaluationState) \
            -> dict[SealedActivation, Any]:
        """Alter the evaluation state to evaluate the underlying graph.

        Parameters
        ----------
        evaluation_state
            Instance of evaluation state, whose graph is evaluated.

        Returns
        -------
            Dictionary which maps childless Activations of the graph to their
            results.
        """

        self._evaluation_state = evaluation_state
        while node_to_process := self._get_node_to_process():
            # TODO: update swap order before 'forgetting' the search order
            self._necessary = []
            self._visited = []
            self._process(node_to_process)

        results = self._get_algorithm_result()
        return results

    def _get_node_to_process(self):
        """Get next node to process.

        Returns
        -------
            Next node to process or None, if there are none nodes to process.
        """

        if self._evaluation_state.objectives:
            nodes_to_process = self._evaluation_state.objectives
        else:
            nodes_to_process = [node
                                for node in self._evaluation_state.results
                                if not self._is_processed(node)]

        try:
            next_node = next(iter(nodes_to_process))
            return next_node
        except StopIteration:
            return None

    @staticmethod
    def _is_processed(node):
        """Whether the node is processed.

        Processed nodes are the ones either in MEMORY or DISK state.

        Parameters
        ----------
        node
            The examined node.

        Returns
        -------
            True, if the node is processed, i.e. either in MEMORY or DISK
            state. Otherwise False.
        """

        return node.state is DataNodeState.MEMORY \
            or node.state is DataNodeState.DISK

    def _process(self, node):
        """Process the given node.

        If the node need not to be evaluated (data on disk or in database),
        then it is easy. Otherwise, DFS is used for processing the parents of
        the node.

        The method modifies the `_necessary` and `_processed` attributes.
        After return, the `_necessary` field has appended the node,
        the `_processed` field is extended by visited node's descendants in
        post-order traversal (including the node itself).

        Parameters
        ----------
        node
            Node to process, see `_is_processed` method.
        """

        # If node is not already processed
        if not self._is_processed(node):
            # If node has data in database (i.e. load was successful)
            if node.state is DataNodeState.UNKNOWN and node.try_load():
                pass  # Now node.state == MEMORY
            else:
                # Now node.state == NO_DATA and needs to be evaluated
                # Get parents data
                for parent in node.parents:
                    self._process(parent)  # DFS recursion
                # Load the nodes in case they were swapped to disk
                self._load_nodes(node.parents)
                node.evaluate()
                for parent in reversed(node.parents):
                    assert parent is self._necessary.pop()  # Parents were used
            new_data_in_memory = True
        else:
            # Processed nodes
            new_data_in_memory = False

        # Insert the node to structures describing the processing state
        self._necessary.append(node)
        self._visited.append(node)

        # Check the limit, if new data arrived to memory
        if new_data_in_memory and self._too_much_memory():
            self._save_memory()

    def _load_nodes(self, nodes):
        """Ensure that the given nodes are in MEMORY state.

        It is guaranteed that the nodes will be in MEMORY after return from
        the function. However, any call to `_save_memory` method may break the
        condition.

        Parameters
        ----------
        nodes
            The nodes to get to the MEMORY state. They must be processed,
            see `_is_processed` method.
        """

        for node in nodes:
            if node.state is DataNodeState.MEMORY:
                continue
            elif node.state is DataNodeState.DISK:
                node.load()
                if self._too_much_memory():
                    self._save_memory(nodes)
            else:
                raise ValueError(f'The node {node} must be either in MEMORY '
                                 f'or DISK state.')

    def _save_memory(self, nodes_to_keep=()):
        """Move some nodes from MEMORY state to DISK state.

        The order of nodes to swap is given by the `_get_swap_order` method.
        The method guarantees preserving the state of nodes from the given list.

        The method removes the nodes from the `_previous_order`, so they are
        not included next time (unless they get there by an other way).

        Parameters
        ----------
        nodes_to_keep
            The nodes, whose state will be preserved, including the case when
            they are in the MEMORY state.
        """

        self._update_swap_order()
        # TODO
        total_used_memory_estimate = sum(node.data_size
                                         for node in self._swap_order)
        # Swap **some** nodes
        # Remove them from the order

    def _update_swap_order(self):
        """Update order in which the nodes should be swapped.

        The order is based on the previous order which is updated with
        processing state of the current node. That is, by fields `_processed`
        and `_necessary`. More info on that is in the code.

        The order has some nice properties, such as the parents of the last
        visited node are last, i.e. they should be swapped last.
        """

        # It is chance that the first visited nodes are roots of the graph
        # Hence, it is a big chance of their re-use
        # Thus, they go last
        self._swap_order.extend(reversed(self._visited))
        # We definitely do not swap the necessary nodes
        # The last in necessary are the first which will be used in _process
        # method
        # Thus, they go last
        self._swap_order.extend(self._necessary)
        # Keep only the last occurrences
        # The further the element occurs, the more important the node's data are
        new_order = collections.deque(
            self._leave_only_last_occurrence(self._swap_order)
        )
        self._swap_order = new_order
        return new_order

    @staticmethod
    def _leave_only_last_occurrence(order: Sequence[DataNode]) \
            -> Iterator[DataNode]:
        """Leave only the last occurrence of each element.

        Parameters
        ----------
        order
            Sequence of nodes, possibly with repeated occurrences of some
            of them.

        Returns
        -------
            Iterator of the nodes with a single occurrence of each. Only the
            last occurrences are preserved.
        """

        # IDEA: If it is too slow, get better algorithm
        # Reverse back, so we have the proper order
        filtered_order = reversed(
            # Preserve first occurrence in reversed deque
            # (i.e. last in the original)
            dict.fromkeys(
                reversed(order)
            )
        )
        return filtered_order

    def _too_much_memory(self):
        """True, if the consumed virtual memory exceeds the memory limit."""
        return self._evaluation_state.used_virtual_memory > self._memory_limit

    def _get_algorithm_result(self):
        """Return the expected result of EvaluationAlgorithm's evaluate method.

        Returns
        -------
            Dictionary which maps childless Activations of the graph to their
            results.
        """

        self._load_nodes(self._evaluation_state.results)
        result = {node.activation: node.get_data()
                  for node in self._evaluation_state.results}
        return result
