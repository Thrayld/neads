from __future__ import annotations

from typing import TYPE_CHECKING

from neads._internal_utils.plain_graph_wrappers import \
    Plain1In1RGraphWrapper

if TYPE_CHECKING:
    from neads.activation_model import ActivationGraph, SealedActivation, \
        SealedActivationGraph


class Choice(Plain1In1RGraphWrapper):
    """A way of performing a step of computation."""

    def __init__(self, graph: ActivationGraph):
        """Initialize Choice with its graph.

        Parameters
        ----------
        graph
            The graph which represent the operations of the Choice. It has
            one input and one result Activation (i.e. single childless
            Activation) and does not have a trigger method (nor its
            Activations).

        Raises
        ------
        ValueError
            If the graph does not have one input and one result Activation.
            If the graph has a trigger method.
        """

        super().__init__(graph)

    def attach(self, target_graph: SealedActivationGraph,
               parent_activation: SealedActivation) -> SealedActivation:
        """Attach the graph to the given graph and its Activation.

        Parameters
        ----------
        target_graph
            The graph to which will be the choice attached.
        parent_activation
            The Activation to which will be the choice attached.

        Returns
        -------
            The Activation of target graph, to which is mapped the result
            Activation of the wrapper's graph.
        """

        return super().attach(target_graph, parent_activation)
