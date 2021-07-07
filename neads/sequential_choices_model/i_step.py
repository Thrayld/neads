from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Sequence
import abc

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph, SealedActivation
    from neads.sequential_choices_model.tree_view import TreeView


class IStep(abc.ABC):
    """General API for SCM's step.

    The IStep subclasses represent a step in computation. The step can be
    performed by one or more ways, usually called choices.
    """

    @abc.abstractmethod
    def create(self,
               target_graph: SealedActivationGraph,
               parent_activation: SealedActivation,
               tree_view: TreeView,
               next_steps: Sequence[IStep]):
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

    @staticmethod
    def _create_next_steps(target_graph: SealedActivationGraph,
                           step_results: Iterable[SealedActivation],
                           tree_view: TreeView,
                           next_steps: Sequence[IStep]):
        """Let create the next steps their portion of the graph.

        Parameters
        ----------
        target_graph
            The graph to which will be the Activations added,
            i.e. `target_graph` argument for the `create` method of the next
            steps.
        step_results
            All result Activation of the given step, i.e. the added children
            to the tree view. Each of these Activations will serve as
            `parent_activation` argument for the create method of the next
            steps.
        tree_view
            The TreeView of the `target_graph`.
        next_steps
            The next steps to create. It may be empty.
        """

        if len(next_steps) > 0:
            next_step = next_steps[0]
            following_steps = next_steps[1:]
            for result_act in step_results:
                next_step.create(target_graph, result_act, tree_view,
                                 following_steps)
