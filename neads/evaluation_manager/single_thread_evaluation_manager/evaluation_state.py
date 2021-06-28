from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Iterator, Iterable
import collections.abc

import neads.utils.memory_info as memory_info
from neads.evaluation_manager.single_thread_evaluation_manager.data_node \
    import DataNode, DataNodeState
from neads.evaluation_manager.single_thread_evaluation_manager \
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
            the data were found right away). The database is supposed to be
            open.
        """

        self._activation_graph = activation_graph
        self._database = database

        # If the ES is in complete state, i.e. the graph contains some triggers
        self._is_complete = False

        # Some fields
        self._top_level = []
        self._objectives = []
        self._results = []

        # Nodes by state
        self._nodes_by_state: dict[DataNodeState, set[DataNode]] = \
            collections.defaultdict(set)

        # Important mappings
        self._act_to_node: dict[SealedActivation, DataNode] = {}
        self._node_to_act: dict[DataNode, SealedActivation] = {}

        # Helper for tracking eligible activations with trigger-on-descendants
        self._trigger_detector = EligibilityDetector(self._activation_graph)

        # Creating data nodes and incorporating them
        self._incorporate_activations(list(self._activation_graph))

        # Checking if some triggers are already eligible to be called
        self._invoke_eligible_non_result_triggers()

    def _incorporate_activations(self, activations):
        """Incorporate the given Activations to State's data structures.

        The Activations are considered to be new to the graph, thus,
        the corresponding nodes are created.

        The method does not update the `trigger_detector`
        """

        nodes = self._get_new_data_nodes(activations)

        # Extending some fields
        self._top_level.extend(node for node in nodes if node.level == 0)
        self._objectives.extend(node for node in nodes
                                if node.has_trigger_on_result)

        # All new nodes are UNKNOWN
        self._nodes_by_state[DataNodeState.UNKNOWN].update(nodes)

    def _get_new_data_nodes(self, activations) -> list[DataNode]:
        """Create DataNodes for the given activations with assigned callbacks.

        Returns
        -------
            Mapping of Activations to created DataNodes, which have set their
            callbacks.
        """

        created_nodes = self._create_data_nodes_and_extend_mappings(activations)
        for node in created_nodes:
            self._register_callbacks(node)
        return created_nodes

    def _create_data_nodes_and_extend_mappings(self, activations) \
            -> list[DataNode]:
        """Create DataNodes for the given Activations and extent ES's mappings.

        The method extends the ES's `act_to_node` and `node_to_act` mappings.

        Returns
        -------
            Created DataNodes for the given Activations.
        """

        ordered_activations = sorted(activations,
                                     key=lambda act: act.level)
        created_nodes = []

        for activation in ordered_activations:
            parent_nodes = [self._act_to_node[act]
                            for act in activation.parents]
            created_node = DataNode(activation, parent_nodes, self._database)
            self._act_to_node[activation] = created_node
            self._node_to_act[created_node] = activation
            created_nodes.append(created_node)

        return created_nodes

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
        return self._get_general_callback(
            DataNodeState.UNKNOWN,
            DataNodeState.NO_DATA
        )

    def _get_callback_unknown_to_memory(self):
        return self._get_general_callback(
            DataNodeState.UNKNOWN,
            DataNodeState.MEMORY,
            invoke_trigger=True
        )

    def _get_callback_no_data_to_memory(self):
        return self._get_general_callback(
            DataNodeState.NO_DATA,
            DataNodeState.MEMORY,
            invoke_trigger=True
        )

    def _get_callback_memory_to_disk(self):
        return self._get_general_callback(
            DataNodeState.MEMORY,
            DataNodeState.DISK
        )

    def _get_callback_disk_to_memory(self):
        # For DISK to MEMORY transition, the node had been in MEMORY before
        # Thus, its potential trigger-on-result was already invoked
        return self._get_general_callback(
            DataNodeState.DISK,
            DataNodeState.MEMORY
        )

    def _get_general_callback(self, state_from, state_to, *,
                              invoke_trigger: bool = False):
        """Create general callback for DataNode's transition between states.

        Parameters
        ----------
        state_from
            State from which the node transits.
        state_to
            State to which the node transits.
        invoke_trigger
            Whether invoke the trigger-on-result of the given node, if exists.
            It sets off (potentially) a cascade of trigger invocations
            (trigger-on-descendants, graph's). The check is meaningless and
            does not occur, if the ES is complete.
        """

        def callback(data_node: DataNode):
            # Move node inside the ES's data structures
            self._nodes_by_state[state_from].remove(data_node)
            self._nodes_by_state[state_to].add(data_node)

            if not self._is_complete:
                # If requested, set off the trigger invocation
                if invoke_trigger and data_node.has_trigger_on_result:
                    self._process_trigger_on_result(data_node)
                    self._invoke_eligible_non_result_triggers()

        return callback

    def _process_trigger_on_result(self, data_node):
        """Process the trigger-on-result of the given node.

        Parameters
        ----------
        data_node
            The node whose trigger-on-result method will be invoked and
            its result processed.
        """

        processed_activation = self._node_to_act[data_node]
        self._process_general_trigger(processed_activation,
                                      'trigger_on_result',
                                      data_node.get_data())
        self._objectives.remove(data_node)

    def _process_trigger_on_descendants(self, data_node):
        """Process the trigger-on-descendants of the given node.

        Parameters
        ----------
        data_node
            The node whose trigger-on-descendants method will be invoked and
            its result processed.
        """

        processed_activation = self._node_to_act[data_node]
        self._process_general_trigger(processed_activation,
                                      'trigger_on_descendants')

    def _process_graph_trigger(self):
        """Process the graph's trigger."""
        self._process_general_trigger(self._activation_graph, 'trigger_method')

    def _process_general_trigger(self, obj, trigger_name: str, *trigger_args):
        """General method for trigger processing.

        It appropriately calls the described trigger method (i.e. removes it
        from the object first) and processes the its result (incorporates
        activations and updates the trigger detector).

        Parameters
        ----------
        obj
            Object whose trigger method is processed.
        trigger_name
            Name of the obj's trigger method to process.
        trigger_args
            Arguments for the trigger method. Nothing for graph's trigger and
            trigger-on-descendants. The result of the corresponding plugin
            for the trigger-on-result method.
        """

        # Initialization
        trigger = getattr(obj, trigger_name)
        delattr(obj, trigger_name)

        # Invocation
        new_activations = trigger(*trigger_args)

        # Finish
        self._incorporate_activations(new_activations)
        self._trigger_detector.update(obj, new_activations)

    def _invoke_eligible_non_result_triggers(self):
        """Successively invoke all eligible triggers-on-descendants and graph's.

        The method invokes as much trigger-on-descendants as possible. If
        graph's trigger is present and its invocation is eligible, the method
        continues with it. Then it starts recursion (again checking
        trigger-on-descendants methods).

        If the graph's trigger is not present, then the ES switches to
        complete state.
        """

        # Process all eligible trigger-on-descendants methods
        while self._trigger_detector.eligible_activations:
            eligible_activation = \
                self._trigger_detector.eligible_activations[0]
            self._process_trigger_on_descendants(
                self._act_to_node[eligible_activation]
            )

        # No eligible Activations with trigger-on-descendants

        # Are there any other Activations' trigger methods?
        # It is sufficient to look only at trigger-on-result, because if
        # there is no eligible trigger-on-descendants, then either no such
        # method is present or a trigger-on-descendants is 'blocked' (made
        # ineligible) by a trigger-on-result
        if len(self._objectives):
            # Nothing we can do right now
            # No eligible activation and graph's trigger (if exists) is blocked
            return
        else:
            # Check presence of graph's trigger
            if self._activation_graph.trigger_method:
                # Process the graphs trigger and repeat the check
                self._process_graph_trigger()
                self._invoke_eligible_non_result_triggers()
            else:
                self._switch_to_complete_state()

    def _switch_to_complete_state(self):
        """Switch the EvaluationState to 'complete' state.

        The complete state means that no trigger methods are present in the
        graph. Thus, it cannot be further modified.

        That is, the method is supposed to be called only after all trigger
        methods were invoked.
        """

        self._results = [node for node in self if len(node.children) == 0]
        self._is_complete = True

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
