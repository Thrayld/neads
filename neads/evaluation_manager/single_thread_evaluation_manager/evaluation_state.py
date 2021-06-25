from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Iterator, Iterable
import collections.abc

import neads.utils.memory_info as memory_info
from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
    import DataNode, DataNodeState
from neads.evaluation_manager.single_thread_evaluation_manager\
    .eligibility_detector import EligibilityDetector

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph, SealedActivation
    from neads.database import IDatabase


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
            # TODO: opened or closed?
        """

        # TODO: do not forget some initial triggers

        self._activation_graph = activation_graph
        self._database = database

        # Creating nodes and important mappings
        self._act_to_node: dict[SealedActivation, DataNode] = \
            self._get_data_nodes()
        self._node_to_act: dict[DataNode, SealedActivation] = \
            {node: act for act, node in self._act_to_node.items()}
        nodes = self._act_to_node.values()

        # Creating helper for checking eligible trigger-on-descendants
        self._trigger_detector = EligibilityDetector(self._activation_graph)

        # Initializing some fields
        self._top_level = [node for node in nodes if node.level == 0]
        self._objectives = [node for node in nodes
                            if node.has_trigger_on_result]
        self._results = []

        # Categorizing nodes by state
        self._nodes_by_state: dict[DataNodeState, set[DataNode]] = \
            collections.defaultdict(set)
        self._nodes_by_state[DataNodeState.UNKNOWN] = \
            set(nodes)

    def _incorporate_activations(self, activations):
        """Incorporate the given Activations to State's data structures.

        It involves creating DataNodes from the Activations and so on.
        """

    def _get_data_nodes(self):
        """Create DataNodes for given graph and assign them the callbacks.

        Returns
        -------
            Mapping of Activations to created DataNodes, which have set their
            callbacks.
        """

        act_to_node = self._create_data_nodes()
        for node in act_to_node.values():
            self._register_callbacks(node)
        return act_to_node

    def _create_data_nodes(self):
        """Create DataNodes for Activations of the given graph.

        Returns
        -------
            Mapping of Activations to created DataNodes.
        """

        ordered_activations = sorted(self._activation_graph,
                                     key=lambda act: act.level)
        act_to_node: dict[SealedActivation, DataNode] = {}

        for activation in ordered_activations:
            parent_nodes = [act_to_node[act] for act in activation.parents]
            created_node = DataNode(activation, parent_nodes, self._database)
            act_to_node[activation] = created_node

        return act_to_node

    def _register_callbacks(self, data_node):
        """Register callbacks to the given DataNode.

        A callback will be registered for each of 5 allowed transitions of
        DataNode's state.

        Parameters
        ----------
        data_node
            The DataNode where the callbacks will be registered.
        """

        data_node.register_callback_unknown_to_no_data(
            self._get_callback_unknown_to_no_data()
        )
        data_node.register_callback_unknown_to_memory(
            self._get_callback_unknown_to_memory()
        )
        data_node.register_callback_no_data_to_memory(
            self._get_callback_no_data_to_memory()
        )
        data_node.register_callback_memory_to_disk(
            self._get_callback_memory_to_disk()
        )
        data_node.register_callback_disk_to_memory(
            self._get_callback_disk_to_memory()
        )

    def _get_callback_unknown_to_no_data(self):
        def callback(data_node: DataNode):
            self._move_node_after_state_change(data_node,
                                               DataNodeState.UNKNOWN,
                                               DataNodeState.NO_DATA)
        return callback

    def _get_callback_unknown_to_memory(self):
        # Watch for triggers

        def callback(data_node: DataNode):
            if data_node.has_trigger_on_result:
                ...  # call it
                self._invoke_eligible_triggers()
            self._move_node_after_state_change(data_node,
                                               DataNodeState.UNKNOWN,
                                               DataNodeState.MEMORY)
        return callback

    def _get_callback_no_data_to_memory(self):
        # Watch for triggers

        def callback(data_node: DataNode):
            if data_node.has_trigger_on_result:
                ...  # call it
                self._invoke_eligible_triggers()
            self._move_node_after_state_change(data_node,
                                               DataNodeState.NO_DATA,
                                               DataNodeState.MEMORY)
        return callback

    def _get_callback_memory_to_disk(self):
        def callback(data_node: DataNode):
            self._move_node_after_state_change(data_node,
                                               DataNodeState.MEMORY,
                                               DataNodeState.DISK)
        return callback

    def _get_callback_disk_to_memory(self):
        # For DISK to MEMORY transition, the node had been in MEMORY before
        # Thus, its potential trigger-on-result was already invoked
        def callback(data_node: DataNode):
            self._move_node_after_state_change(data_node,
                                               DataNodeState.DISK,
                                               DataNodeState.MEMORY)
        return callback

    def _move_node_after_state_change(self, data_node, state_from, state_to):
        """Move the given node between structures for nodes in particular state.

        Parameters
        ----------
        data_node
            Node which state was changed.
        state_from
            State from which the node transits.
        state_to
            State to which the node transits.
        """

        self._nodes_by_state[state_from].remove(data_node)
        self._nodes_by_state[state_to].add(data_node)

    def _process_trigger_on_result(self, data_node):
        """Process trigger-on-result of the given DataNode.

        The method calls the trigger and updates the EvaluationState by the
        triggers result (i.e. the new graph's Activations).

        Parameters
        ----------
        data_node
            The DataNode in MEMORY state whose trigger-on-result will be
            processed.
        """

        corresponding_activation = self._node_to_act[data_node]
        trigger = corresponding_activation.trigger_on_result
        del corresponding_activation.trigger_on_result

        new_activations = trigger(data_node.get_data())




    def _invoke_eligible_triggers(self):
        """Successively invoke all eligible triggers-on-descendants and graph's.

        The trigger-on-result methods are handler separately.
        """

        pass

    @property
    def used_virtual_memory(self) -> int:
        """The amount of used virtual memory by the process

        Includes swap memory etc.
        """

        return memory_info.get_process_virtual_memory()

    @property
    def used_physical_memory(self) -> int:
        """The amount of RAM memory currently used by the process.

        Very much depends on the system swapping policy.
        """

        return memory_info.get_process_ram_memory()

    @property
    def available_memory(self) -> int:
        """The amount of free memory in bytes left to allocate.

        More precisely, it is the memory that can be given instantly to
        processes without the system going into swap.
        """

        return memory_info.get_available_memory()

    @property
    def memory_nodes(self) -> Iterable[DataNode]:
        """Data nodes in the state MEMORY."""
        return self._nodes_by_state[DataNodeState.MEMORY]

    @property
    def disk_nodes(self) -> Iterable[DataNode]:
        """Data nodes in the state DISK."""
        return self._nodes_by_state[DataNodeState.DISK]

    @property
    def no_data_nodes(self) -> Iterable[DataNode]:
        """Data nodes in the state MEMORY."""
        return self._nodes_by_state[DataNodeState.NO_DATA]

    @property
    def unknown_nodes(self) -> Iterable[DataNode]:
        """Data nodes in the state UNKNOWN."""
        return self._nodes_by_state[DataNodeState.UNKNOWN]

    @property
    def objectives(self) -> Iterable[DataNode]:
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

        return self._objectives

    @property
    def results(self):
        """Data nodes whose data are the result of computation.

        The childless nodes, whose data are the result of computation. Thus,
        they need to have their data evaluated (or loaded from DB).

        The nodes are shown only when it is certain that they are (and will
        be) childless. That is, after all the trigger methods were called and
        no new Activations can appear in the graph. Before that, empty iterable
        is returned.
        """

        return self._results

    @property
    def has_graph_trigger(self):
        """Whether the corresponding graph has a trigger method."""
        return bool(self._activation_graph.trigger_method)

    @property
    def top_level(self) -> Iterable[DataNode]:
        """Return iterable of all DataNodes on level 0.

        The top DataNodes are exactly all the DataNodes without parents.

        Returns
        -------
            The iterable of all DataNodes on level 0.
        """

        # TODO: do not forget update them after trigger invocation, although
        #  it is a bit unlikely
        return self._top_level

    def __iter__(self) -> Iterator[DataNode]:
        """Iterate over all DataNodes of the underlying graph.

        Note that performing actions that changes the state may result in
        undefined behavior.

        Returns
        -------
            An iterator over all DataNodes in the EvaluationState.
        """

        return itertools.chain(*self._nodes_by_state.values())
