from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neads.activation_model import ActivationGraph, SealedActivation, \
        SealedActivationGraph


class Choice:
    """A way of performing a step of computation."""

    def __init__(self, activation_graph: ActivationGraph):
        """Initialize Choice with its graph.

        Parameters
        ----------
        activation_graph
            The graph which represent the operations of the Choice. It has
            one input and one result Activation (i.e. single childless
            Activation).
        """

        raise NotImplementedError()

    def attach(self, target_graph: SealedActivationGraph,
               parent_activation: SealedActivation):
        """Attach the graph to the given graph and its Activation.

        Parameters
        ----------
        target_graph
            The graph to which will be the choice attached.
        parent_activation
            The Activation to which will be the choice attached.
        """

        raise NotImplementedError()
