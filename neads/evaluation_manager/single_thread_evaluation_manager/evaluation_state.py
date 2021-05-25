from typing import TYPE_CHECKING
import collections.abc

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph
    from neads.database import Database
    from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
        import DataNode


class EvaluationState(collections.abc.Iterable):
    """Hold the state of evaluation and enable its modification.

    State of evaluation consists of states of individual Activations of an
    ActivationGraph represented by DataNodes. Also, location of trigger
    methods contributes to the state.

    EvaluationState holds of information related to the state of evaluation
    and presents them in convenient form. Also, EvaluationState provides
    methods for alternation of the state, which hide the technical details from
    the user of EvaluationState.
    """

    def __init__(self,
                 activation_graph: SealedActivationGraph,
                 database: Database,
                 memory_limit: int):
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
        memory_limit
            Soft limit on the amount of memory in bytes which is allowed to be
            consumed by the current process during evaluation.

            This parameter serves as an additional piece of information to
            the EvaluationState API and serves as recommendation for the user
            of EvaluationState to adapt the evaluation accordingly.
        """

        raise NotImplementedError()

    @property
    def free_memory(self):
        """The amount of free memory in bytes left to allocate.

        free_memory = memory_limit - total_used_memory
        """
        raise NotImplementedError()

    @property
    def used_memory(self):
        """The amount of memory in bytes used by data of Activations.

        The rest (i.e. total_used_memory - used_memory) cannot be removed
        from memory via EvaluationState.
        """
        raise NotImplementedError()

    @property
    def total_used_memory(self):
        """Total amount of memory in bytes used by data of the process."""
        raise NotImplementedError()

    @property
    def memory_limit(self):
        """Soft limit on the amount of memory to be consumed by the process.

        In bytes.
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
    def trigger_nodes(self):
        """Data nodes with trigger, which are necessary to get to MEMORY state.

        Trigger methods need to called sometime. They expand the graph and
        therefore the evaluation depends on them. To call the trigger method
        of a node, the node must be set to MEMORY state. The method is then
        called automatically by the EvaluationState.

        The other trigger methods are called by EvaluationState in
        appropriate moment as well. But the user of EvaluationState need not
        to care about them.
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
    def has_trigger(self):
        """Whether the corresponding graph has a trigger method."""
        raise NotImplementedError()

    def get_top_level(self) -> tuple[DataNode]:
        """Return list of all DataNodes on level 0.

        The top DataNodes are exactly all the DataNodes without parents.

        Returns
        -------
            The list of all DataNodes on level 0.
        """
        raise NotImplementedError()

    def __iter__(self):
        """Iterate over the DataNodes.

        Note that performing actions that changes the state may result in
        undefined behavior.

        Returns
        -------
            An iterator over all DataNodes in the EvaluationState.
        """

        raise NotImplementedError()
