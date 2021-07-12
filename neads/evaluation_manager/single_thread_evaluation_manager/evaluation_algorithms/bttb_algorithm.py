from __future__ import annotations

from typing import TYPE_CHECKING, Any

from neads.evaluation_manager.single_thread_evaluation_manager \
    .evaluation_algorithms.i_evaluation_algorithm import IEvaluationAlgorithm

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation
    from neads.evaluation_manager.single_thread_evaluation_manager \
        .evaluation_state import EvaluationState


# TODO: delete

class BttbAlgorithm(IEvaluationAlgorithm):
    """Algorithm running repeatedly from bottom to top and top to bottom.

    As said, the algorithm has two repeating phases.
    First, it process the nodes from bottom to top. That is, the algorithm
    finds the bottom most nodes and tries to load them. If it does not
    succeed it loads recursively their parents until succeeds (all parents of
    a node are in MEMORY state; including the case when the node has no
    parents). Therefore, the algorithm runs from bottom to top.
    Then, in the second phase, it evaluates the nodes which was not able to
    load previously. That is, the algorithm runs from top to bottom.
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
