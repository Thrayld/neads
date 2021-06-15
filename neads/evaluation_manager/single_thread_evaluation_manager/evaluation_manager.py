from typing import TYPE_CHECKING, Iterable, Any

from ..i_evaluation_manager import IEvaluationManager

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph, SealedActivation
    from neads.database import IDatabase


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

    def evaluate(self, activation_graph: SealedActivationGraph) \
            -> Iterable[tuple[SealedActivation, Any]]:
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

        Returns
        -------
            Iterable collection which contain a tuple for each childless
            Activation in the evaluated graph. Each tuple is a pair of the
            Activation and its data (of any type).
        """

        raise NotImplementedError()
