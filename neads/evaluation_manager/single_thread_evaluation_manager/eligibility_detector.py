from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Deque, Sequence
import collections

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation, SealedActivationGraph


class ActivationEligibilityDetector:
    """Detect eligibility for invocation of Activation's trigger-on-descendant.

    The trigger-on-descendant of an Activation is eligible for invocation is
    no descendant of the Activation has a trigger (of any kind).

    The detector is supposed to be created and used when the graph to which the
    Activation belongs is ready for evaluation. That is, the only way the
    graph is modified is via invocation of a trigger method.

    Then, the detector must be informed about such changes via `update`
    method.
    """

    def __init__(self, activation: SealedActivation):
        """Initialize the instance with the tracked Activation.

        Parameters
        ----------
        activation
            The Activation whose trigger-on-descendant method will be tracked.
        """

        self._activation = activation
        # IDEA: only a direct blockers should suffice
        self._blockers = self._get_descendants_with_trigger()

    @property
    def is_eligible(self):
        """Whether the trigger is eligible for invocation.

        Returns
        -------
            True, it the Activation's trigger-on-descendant is eligible for
            invocation. False, if it is not. None, if the Activation does not
            have assigned any trigger-on-result method.
        """

        if self._activation.trigger_on_descendants is not None:
            return not len(self._blockers)
        else:
            return None

    @property
    def activation(self):
        """The Activation whose trigger is watched."""
        return self._activation

    def update(self, invoked_activation: SealedActivation,
               new_activations: Iterable[SealedActivation]):
        """Update the detector after invocation of other trigger method.

        Invocation of an other trigger method may affect eligibility of the
        tracked method. The Activation whose trigger for called is likely to
        lose its trigger (only trigger-on-descendants can be reset). On the
        other hand, some of the new Activations may have their trigger assigned.

        Parameters
        ----------
        invoked_activation
            The Activation whose trigger was invoked.
        new_activations
            New Activations created by the invoked trigger method.
        """

        # IDEA: I wish more effective implementation using the knowledge of
        #  the Activation with invoked trigger and the new Activations
        #  e.g. searching from these new vertices using parents (utilizing
        #  the fact that usual AG will we kind of a tree)
        self._blockers = self._get_descendants_with_trigger()

    def _get_descendants_with_trigger(self):
        # Initialize data structures for graph search
        acts_to_process: Deque[SealedActivation] = collections.deque()
        # We start searching from Activation's children to avoid addition of
        # the Activation to `desc_with_trigger` list
        acts_to_process.extend(self._activation.children)
        visited = set()
        desc_with_trigger = []

        def does_have_trigger(activation):
            return activation.trigger_on_result \
                   or activation.trigger_on_descendants

        # BFS
        while len(acts_to_process):
            processed_act = acts_to_process.popleft()

            if does_have_trigger(processed_act):
                desc_with_trigger.append(processed_act)

            for child in processed_act.children:
                if child not in visited:
                    acts_to_process.append(child)

        return desc_with_trigger


class EligibilityDetector:
    """Detect trigger-on-descendant methods eligible for invocation.

    The trigger-on-descendant of an Activation is eligible for invocation is
    no descendant of the Activation has a trigger (of any kind).

    The detector is supposed to be created and used when the graph to which the
    Activation belongs is ready for evaluation. That is, the only way the
    graph is modified is via invocation of a trigger method.

    Then, the detector must be informed about such changes via `update`
    method.
    """

    def __init__(self, graph: SealedActivationGraph):
        """Initialize the instance with the tracked graph.

        Parameters
        ----------
        graph
            The graph, whose Activations (their trigger-on-descendants
            method) will be tracked (i.e. checked for eligibility).
        """

        self._graph = graph
        self._activations_detectors = {
            act: ActivationEligibilityDetector(act)
            for act in self._graph
            if act.trigger_on_descendants
        }

    @property
    def graph(self):
        """The graph whose Activations' triggers are watched."""
        return self._graph

    @property
    def eligible_activations(self) -> Sequence:
        """Return Activations whose triggers are eligible for invocation.

        Returns
        -------
            Return Activations whose trigger-on-descendants methods are
            eligible for invocation.
        """

        return tuple(
            act
            for act, detector in self._activations_detectors.items()
            if detector.is_eligible
        )

    @property
    def tracked_activations(self) -> Sequence:
        """Return all tracked Activations.

        Returns
        -------
            All tracked Activations. That is, the Activations with a
            trigger-on-descendants.
        """

        return tuple(self._activations_detectors.keys())

    def update(self, invoked_activation: SealedActivation,
               new_activations: Iterable[SealedActivation]):
        """Update the detector after invocation a trigger method.

        Invocation of a trigger method may affect eligibility of the tracked
        methods. The Activation whose trigger for called is likely to
        lose its trigger (only trigger-on-descendants can be reset). On the
        other hand, some of the new Activations may be given theirs trigger.

        Parameters
        ----------
        invoked_activation
            The Activation whose trigger was invoked.
        new_activations
            New Activations created by the invoked trigger method.
        """

        # Trigger methods cannot modify trigger methods of existing Activations
        # Thus, the Activation tracking can quit only after its invocation,
        # unless the trigger-on-descendants is (re-)set.
        if not invoked_activation.trigger_on_descendants:
            self._activations_detectors.pop(invoked_activation, None)

        # Some of the new Activation may have assigned a trigger-on-descendants
        # Thus, if new Activation have this trigger, we start its tracking
        for new_act in new_activations:
            if new_act.trigger_on_descendants:
                self._activations_detectors[new_act] = \
                    ActivationEligibilityDetector(new_act)

        # Now update the whole pack
        for detector in self._activations_detectors.values():
            detector.update(invoked_activation, new_activations)
