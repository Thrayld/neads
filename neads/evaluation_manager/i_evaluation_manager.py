import abc

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..activation_model import SealedActivationGraph, SealedActivation


class IEvaluationManager(abc.ABC):
    """General interface for EvaluationManagers.

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

        Returns
        -------
            Dictionary which maps childless Activations of the graph to their
            results.
        """
