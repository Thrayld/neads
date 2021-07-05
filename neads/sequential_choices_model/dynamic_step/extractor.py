from __future__ import annotations

from typing import TYPE_CHECKING

from neads.utils.plain_graph_wrappers import Plain3In1RGraphWrapper

if TYPE_CHECKING:
    from neads.activation_model import ActivationGraph, SealedActivation, \
        SealedActivationGraph


class Extractor(Plain3In1RGraphWrapper):
    """Part of dynamic step, process the subtasks produces by separator.

    The extractor is an ActivationGraph with 3 inputs, the first for the data
    of the Activation which served as input to the separator (i.e. the
    `parent_activation` in create method), the second for data of separator
    and the last for index to the data. The extractor has, as usual,
    one result Activation which is considered to be the result of step's
    choice. That is, step's choices results are the result Activation of
    attached extractors (i.e. they are added as children of the
    `parent_activation` to the TreeView and the next steps are attached to
    them).
    """

    def __init__(self, graph: ActivationGraph):
        """Initialize extractor with its graph.

        Parameters
        ----------
        graph
            The graph which represent the operations of the extractor.
            It has three inputs and one result Activation (i.e. single childless
            Activation) and does not have a trigger method (nor its
            Activations).
            See docstrings of the class and the `attach` method for more on
            the role of each extractor's input.

        Raises
        ------
        ValueError
            If the graph does not have three inputs and one result Activation.
            If the graph has a trigger method.
        """

        super().__init__(graph)

    def attach(self, target_graph: SealedActivationGraph,
               data_activation: SealedActivation,
               instruction_activation: SealedActivation,
               instruction_index: int) -> SealedActivation:
        """Attach the extractor's graph to the given graph.

        Parameters
        ----------
        target_graph
            The graph to which will be the extractor's graph attached.
        data_activation
            The Activation which serves as a data source for the extractor.
            That is, the Activation to which the separator was attached.
            This parameter is realization of the first input of the
            extractor's graph.
        instruction_activation
            The Activation which serves as a instruction source for the
            extractor. That is, the separator's result Activation.
            This parameter is realization of the second input of the
            extractor's graph.
        instruction_index
            Index of the instruction designated for the attached copy
            of extractor. This parameter is realization of the third input of
            the extractor's graph.

        Returns
        -------
            The Activation of target graph, to which is mapped the result
            Activation of the extractor's graph.
        """

        inputs_realizations = [
            data_activation.symbol,
            instruction_activation.symbol,
            instruction_index
        ]
        old_to_new_mapping = target_graph.attach_graph(self._graph,
                                                       inputs_realizations)
        new_result_act = old_to_new_mapping[self._result_act]
        return new_result_act  # noqa: The activation is really a SealedAct
