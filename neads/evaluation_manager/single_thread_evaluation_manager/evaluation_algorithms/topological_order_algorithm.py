from __future__ import annotations

from typing import TYPE_CHECKING, Any

from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_algorithms.i_evaluation_algorithm import IEvaluationAlgorithm
from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
    import DataNodeState


if TYPE_CHECKING:
    from neads.activation_model import SealedActivation
    from neads.evaluation_manager.single_thread_evaluation_manager \
        .evaluation_state import EvaluationState
    from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
        import DataNode


class TopologicalOrderAlgorithm(IEvaluationAlgorithm):
    """Simple algorithm which process the nodes in topological order.

    The algorithm always find the top most unprocessed node which evaluate.

    Simple BFS need not work, as a trigger method may append new node to
    already processed one.
    """

    def evaluate(self, evaluation_state: EvaluationState) \
            -> dict[SealedActivation, Any]:
        """Alter the evaluation state to evaluate the underlying graph.

        The evaluation has two steps.
        First, the algorithm must evaluate all 'objective nodes' (property of
        ES), more precisely gets them to MEMORY state (either by evaluation or
        load from database).
        Then, the algorithm must get data from all 'result nodes' which are
        then returned.

        Parameters
        ----------
        evaluation_state
            Instance of evaluation state, whose graph is evaluated.

        Returns
        -------
            Dictionary which maps childless Activations of the graph to their
            results.
        """

        while node := self._get_next_node_to_process(evaluation_state):
            self._process(node)

        results = {
            node.activation: node.get_data()
            for node in evaluation_state.results
        }

        return results

    def _get_next_node_to_process(self, evaluation_state: EvaluationState):
        """Next node to process.

        Returns
        -------
            Next node to process, i.e. the top most unprocessed node. None,
            if all nodes were processed.
        """

        unprocessed_nodes = [node for node in evaluation_state
                             if self._is_unprocessed(node)]
        if unprocessed_nodes:
            sorted_unprocessed_nodes = sorted(unprocessed_nodes,
                                              key=lambda dn: dn.level)
            return sorted_unprocessed_nodes[0]
        else:
            return None

    @staticmethod
    def _is_unprocessed(data_node: DataNode):
        return data_node.state is DataNodeState.UNKNOWN

    @staticmethod
    def _process(node: DataNode):
        if not node.try_load():
            node.evaluate()
