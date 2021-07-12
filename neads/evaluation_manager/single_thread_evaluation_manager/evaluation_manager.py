from __future__ import annotations

from typing import TYPE_CHECKING, Any
import psutil

from neads.evaluation_manager.i_evaluation_manager import IEvaluationManager
from neads.evaluation_manager.single_thread_evaluation_manager \
    .evaluation_state import EvaluationState
from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_algorithms.complex_algorithm import ComplexAlgorithm
from neads.logging_autoconfig import configure_logging

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
            Database for Activations' data. The database is supposed to be
            closed.
        """

        # raise NotImplementedError()
        self._database = database

    def evaluate(self, activation_graph: SealedActivationGraph,
                 evaluation_algorithm: IEvaluationAlgorithm = None) \
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
            The default algorithm is the ComplexAlgorithm with memory limit
            set to 3/4 of total physical memory (provided by psutil).

        Returns
        -------
            Dictionary which maps childless Activations of the graph to their
            results.
        """

        algorithm = evaluation_algorithm \
            if evaluation_algorithm is not None \
            else self._get_default_algorithm()
        with self._database:
            evaluation_state = EvaluationState(activation_graph, self._database)
            results = algorithm.evaluate(evaluation_state)
        return results

    @staticmethod
    def _get_default_algorithm():
        """Create the default EvaluationAlgorithm.

        Returns
        -------
            ComplexAlgorithm with memory limit set to 1/2 of total physical
            memory (provided by psutil).
        """

        coefficient = 1/2
        memory_limit = psutil.virtual_memory().total * coefficient
        algorithm = ComplexAlgorithm(memory_limit=memory_limit)
        return algorithm
