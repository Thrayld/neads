from __future__ import annotations

from typing import TYPE_CHECKING, Any

from neads.evaluation_manager.i_evaluation_manager import IEvaluationManager

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph, SealedActivation
    from neads.database import IDatabase
    from neads.evaluation_manager.single_thread_evaluation_manager \
        .evaluation_algorithms.i_evaluation_algorithm import \
        IEvaluationAlgorithm


class SingleThreadEvaluationManager(IEvaluationManager):
    """The kind of EvaluationManager that runs in a single thread."""

    def __init__(self, database: IDatabase):
        """Initialize a SingleThreadEvaluationManager instance.

        Parameters
        ----------
        database
            Database for Activations' data.
        """

        raise NotImplementedError()
        # self._database = database

    def evaluate(self, activation_graph: SealedActivationGraph,
                 evaluation_algorithm: IEvaluationAlgorithm) \
            -> dict[SealedActivation, Any]:
        """Evaluate the given graph.

        Evaluation means that all the trigger methods in the graph will be
        evaluated (even of the subsequently created Activations) and data of
        childless Activations will be returned.

        Parameters
        ----------
        activation_graph
            The graph to be evaluated. Note that it may be changed
            (mostly expanded) during the evaluation (as a consequence of
            trigger's evaluation).
        evaluation_algorithm
            The algorithm which will execute the evaluation.

        Returns
        -------
            Dictionary which maps childless Activations of the graph to their
            results.
        """

        raise NotImplementedError()
        # with database ?
        #     es = EvaluationState(graph, database)
        #     alg = EvaluationAlgorithm
