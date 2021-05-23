import abc

from typing import TYPE_CHECKING, Iterable, Any

if TYPE_CHECKING:
    from ..activation_model import SealedActivationGraph, SealedActivation


class EvaluationManager(abc.ABC):
    """General abstract class for EvaluationManagers.

    EvaluationManager is responsible for evaluating given
    SealedActivationGraph. The evaluation usually involves evaluation of
    individual nodes, loading and saving their data to a Database, memory
    management etc. For more info on evaluation see `evaluate` method.

    Only SealedActivationGraphs may be evaluated, as their Activations
    (SealedActivations) possess DataDefinition. For simplification, we use
    the name Activation and ActivationGraph for SealedActivation and
    SealedActivationGraph in the context of EvaluationManager.
    """

    @abc.abstractmethod
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
