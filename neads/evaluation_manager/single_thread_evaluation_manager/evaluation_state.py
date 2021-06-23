from __future__ import annotations

from typing import TYPE_CHECKING, Iterator
import collections.abc

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph
    from neads.database import IDatabase
    from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
        import DataNode


class EvaluationState(collections.abc.Iterable):
    """Hold the state of evaluation and enable its modification.

    State of evaluation consists of states of individual Activations of an
    SealedActivationGraph represented by DataNodes and arrangement of trigger
    methods in the graph.

    EvaluationState holds of information related to the state of evaluation
    and presents them in convenient form. Also, EvaluationState provides
    methods for alternation of the state (more precisely, DataNode instances
    provide these methods).

    One of the greatest responsibilities performed by the EvaluationState
    itself (not via DataNodes; at least from the user's point of view) is
    invocation of Activations' and graph's trigger methods.

    The trigger methods are called as soon as possible. That is,
    the trigger-on-result is called when the DataNode acquires its data. The
    trigger-on-descendants is called as soon as there is no descendant of the
    DataNode which carries a trigger (i.e. after invocation of last
    descendant's trigger, if it does not introduce new Activation with a
    trigger). Note that if more trigger-on-descendant methods are suitable
    for invocation, one of them is chosen first and its invocation (which
    creates new Activations) may block invocation of the other triggers for
    the moment. Similarly with the graph's trigger.
    """

    def __init__(self,
                 activation_graph: SealedActivationGraph,
                 database: IDatabase):
        """Initialize an EvaluationState instance.

        Parameters
        ----------
        activation_graph
            The graph to be evaluated. The EvaluationState instance then
            describes state of evaluation of the graph.
        database
            Database for Activations' data. DataNodes will try to load their
            data from there and save the data there after evaluation (unless
            the data were found right away).
        """

        raise NotImplementedError()

    @property
    def used_virtual_memory(self):
        """The amount of used virtual memory by the process

        Includes swap memory etc.
        """

        raise NotImplementedError()

    @property
    def used_physical_memory(self):
        """The amount of RAM memory currently used by the process.

        Very much depends on the system swapping policy.
        """

        raise NotImplementedError()

    @property
    def available_memory(self):
        """The amount of free memory in bytes left to allocate.

        More precisely, it is the memory that can be given instantly to
        processes without the system going into swap.
        """

        raise NotImplementedError()

    @property
    def memory_nodes(self):
        """Data nodes in the state MEMORY."""
        raise NotImplementedError()

    @property
    def disk_nodes(self):
        """Data nodes in the state DISK."""
        raise NotImplementedError()

    @property
    def no_data_nodes(self):
        """Data nodes in the state MEMORY."""
        raise NotImplementedError()

    @property
    def unknown_nodes(self):
        """Data nodes in the state UNKNOWN."""
        raise NotImplementedError()

    @property
    def objective_nodes(self):
        """Data nodes that are necessary to get to the MEMORY state.

        The objective nodes are exactly those nodes with a trigger-on-result.
        That is, the trigger methods need to called sometime as they expand
        the graph and the process of evaluation depends on them.

        To call the trigger-on-result method of a node, the node must be set
        to MEMORY state. The other types of triggers can be called step by
        step, if no trigger-on-result methods are present.

        The trigger methods are called automatically by the EvaluationState,
        so the user of EvaluationState only needs to get the objective nodes
        to the MEMORY state.

        Note that (obviously) the value of objective nodes may change after
        each invocation of a trigger.
        """

        raise NotImplementedError()

    @property
    def result_nodes(self):
        """Data nodes whose data are the result of computation.

        The childless nodes, whose data are the result of computation. Thus,
        they need to have their data evaluated (or loaded from DB).

        The nodes are shown only when it is certain that they are (and will
        be) childless. That is, after all the trigger methods were called and
        no new Activations can appear in the graph.
        """

        raise NotImplementedError()

    @property
    def has_graph_trigger(self):
        """Whether the corresponding graph has a trigger method."""
        raise NotImplementedError()

    @property
    def top_level(self) -> tuple[DataNode]:
        """Return list of all DataNodes on level 0.

        The top DataNodes are exactly all the DataNodes without parents.

        Returns
        -------
            The list of all DataNodes on level 0.
        """

        raise NotImplementedError()

    def __iter__(self) -> Iterator[DataNode]:
        """Iterate over the DataNodes.

        Note that performing actions that changes the state may result in
        undefined behavior.

        Returns
        -------
            An iterator over all DataNodes in the EvaluationState.
        """

        raise NotImplementedError()
