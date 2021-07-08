from __future__ import annotations

from typing import TYPE_CHECKING
import abc

import neads._internal_utils.graph_utils as graph_utils

if TYPE_CHECKING:
    from neads.activation_model import ActivationGraph, SealedActivation, \
        SealedActivationGraph


class Plain1RGraphWrapper(abc.ABC):
    """Wrapper for graph with one result Activation without triggers.

    Specification of number of inputs is left to the subclass.
    """

    @staticmethod
    @abc.abstractmethod
    def _expected_inputs():
        """Return expected number of graph's inputs."""

    def __init__(self, graph: ActivationGraph):
        """Initialize wrapper with its graph.

        Parameters
        ----------
        graph
            It has one input and one result Activation (i.e. single childless
            Activation) and does not have a trigger method (nor its
            Activations).

        Raises
        ------
        ValueError
            If the graph does not have one input and one result Activation.
            If the graph has a trigger method.
        """

        self._graph = graph

        # Error checking
        graph_utils.assert_inputs_count(self._graph, self._expected_inputs())
        graph_utils.assert_no_triggers(self._graph)
        self._result_act = graph_utils.get_result_activation(self._graph)


class Plain1In1RGraphWrapper(Plain1RGraphWrapper):
    """Wrapper for graph with three inputs and one result without triggers.

    Serves as common base class for some classes requiring ste same
    functionality.
    """

    @staticmethod
    def _expected_inputs():
        """Return expected number of graph's inputs."""
        return 1

    def attach(self, target_graph: SealedActivationGraph,
               parent_activation: SealedActivation) -> SealedActivation:
        """Attach the wrapper's graph to the given graph and its Activation.

        Parameters
        ----------
        target_graph
            The graph to which will be the wrapper's graph attached.
        parent_activation
            The Activation to which will be the wrapper's graph attached.

        Returns
        -------
            The Activation of target graph, to which is mapped the result
            Activation of the wrapper's graph.
        """

        old_to_new_mapping = target_graph.attach_graph(
            self._graph, [parent_activation.symbol])
        new_result_act = old_to_new_mapping[self._result_act]
        return new_result_act  # noqa: The activation is really a SealedAct


class Plain3In1RGraphWrapper(Plain1RGraphWrapper):
    """Wrapper for graph with three inputs and one result without triggers.

    Serves as common base class for some classes requiring ste same
    functionality.
    """

    @staticmethod
    def _expected_inputs():
        """Return expected number of graph's inputs."""
        return 3
