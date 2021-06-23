from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation, SealedActivationGraph


class ActivationEligibilityDetector:
    """Detect eligibility for invocation of Activation's trigger-on-descendant.

    The trigger-on-descendant of an Activation is eligible for invocation is
    no descendant of the Activation has a trigger (of any kind).

    The detector is supposed to be used when the graph to which the
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

        raise NotImplementedError()

    @property
    def is_eligible(self):
        """Whether the trigger is eligible for invocation.

        Returns
        -------
            True, it the Activation's trigger-on-descendant is eligible for
            invocation. False, if it is not. None, if the Activation does not
            have assigned any trigger-on-result method.
        """

        raise NotImplementedError()

    @property
    def activation(self):
        """The Activation whose trigger is watched."""
        raise NotImplementedError()

    def update(self, invoked_activation: SealedActivation,
               new_activations: Iterable[SealedActivation]):
        """Update the detector after invocation of other trigger method.

        Invocation of an other trigger method may affect eligibility of the
        tracked method. The Activation whose trigger for called is likely to
        lose its trigger (only trigger-on-descendants can be reset). On the
        other hand, some of the new Activations may be given theirs trigger.

        Parameters
        ----------
        invoked_activation
            The Activation whose trigger was invoked.
        new_activations
            New Activations created by the invoked trigger method.
        """

        raise NotImplementedError()


class EligibilityDetector:
    """Detect trigger-on-descendant methods eligible for invocation."""

    def __init__(self, graph: SealedActivationGraph):
        """Initialize the instance with the tracked graph.

        Parameters
        ----------
        graph
            The graph, whose Activations (their trigger-on-descendants
            method) will be tracked (i.e. checked for eligibility).
        """

        raise NotImplementedError()

    @property
    def eligible_activations(self):
        """Return Activations whose triggers are eligible for invocation.

        Returns
        -------
            Return Activations whose trigger-on-descendants methods are
            eligible for invocation.
        """

        raise NotImplementedError()

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

        raise NotImplementedError()
