from __future__ import annotations

from typing import TYPE_CHECKING

import neads.utils.graph_utils as graph_utils

if TYPE_CHECKING:
    from neads.activation_model import ActivationGraph, SealedActivation, \
        SealedActivationGraph


class Choice:
    """A way of performing a step of computation."""

    def __init__(self, choice_graph: ActivationGraph):
        """Initialize Choice with its graph.

        Parameters
        ----------
        choice_graph
            The graph which represent the operations of the Choice. It has
            one input and one result Activation (i.e. single childless
            Activation) and does not have a trigger method (nor its
            Activations).

        Raises
        ------
        ValueError
            If the graph does not have one input and one result Activation.
        """

        self._graph = choice_graph

        # Error checking
        graph_utils.assert_inputs_count(self._graph, 1)
        graph_utils.assert_no_triggers(self._graph)
        self._result_act = graph_utils.get_result_activation(self._graph)

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
            Activation of the choice's graph.
        """

        old_to_new_mapping = target_graph.attach_graph(
            self._graph, [parent_activation.symbol])
        new_result_act = old_to_new_mapping[self._result_act]
        return new_result_act  # noqa: The activation is really a SealedAct
