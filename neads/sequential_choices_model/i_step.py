from __future__ import annotations

from typing import TYPE_CHECKING
import abc

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph, SealedActivation


class IStep(abc.ABC):
    """General API for SCM's step.

    The IStep subclasses represent a step in computation. The step can be
    performed by one or more ways, usually called choices.
    """

    @abc.abstractmethod
    def create(self,
               target_graph: SealedActivationGraph,
               parent_activation: SealedActivation,
               tree_view,
               next_steps: list[IStep]):
        """Create the portion of graph described by the step and next steps.

        The step adds new Activations to the given graph a recursively makes the
        following steps create their parts of the graph (note that some parts
        may be created only after invocation of a trigger method).

        Each choice of the can viewed as a subgraph with one input and one
        output Activation (only childless). As the input is used the
        `parent_activation` given to the `create` method. The output Activation,
        on the other hand, is added to the `tree_view` as a child of the
        `parent_activation` and used as an input for the next step (i.e. passed
        as `parent_activation` to the recursive call to the next step).

        Parameters
        ----------
        target_graph
            The graph to which will be the Activations (given by the step and
            the next steps) added.
        parent_activation
            The Activation to which the step's part of the graph is appended.
        tree_view
            The TreeView of the `target_graph`.
        next_steps
            The steps which are supposed to be created at the bottom of the
            part of the graph created by the step.
        """

        pass
