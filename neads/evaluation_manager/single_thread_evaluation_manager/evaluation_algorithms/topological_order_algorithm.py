from __future__ import annotations

from typing import TYPE_CHECKING, Any

from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_algorithms.i_evaluation_algorithm import IEvaluationAlgorithm

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation
    from neads.evaluation_manager.single_thread_evaluation_manager \
        .evaluation_state import EvaluationState


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

        raise NotImplementedError()