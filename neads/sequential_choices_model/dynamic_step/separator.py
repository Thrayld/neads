from __future__ import annotations

from neads._internal_utils.plain_graph_wrappers import \
    Plain1In1RGraphWrapper


class Separator(Plain1In1RGraphWrapper):
    """Part of dynamic step, which determines separation of data to subtasks.

    The separator is an ActivationGraph with one input which and has one result
    Activation. It is attached to the graph first. Then, the length of the
    Activation's data (truly computed by the len() function) determines how
    many times the extractor will be attached to the graph.
    """

    def __init__(self, separator_graph):
        """Initialize Separator with its graph.

        Parameters
        ----------
        separator_graph
            The graph which represent the operations of the Separator. It has
            one input and one result Activation (i.e. single childless
            Activation) and does not have a trigger method (nor its
            Activations).

        Raises
        ------
        ValueError
            If the graph does not have one input and one result Activation.
            If the graph has a trigger method.
        """

        super().__init__(separator_graph)

