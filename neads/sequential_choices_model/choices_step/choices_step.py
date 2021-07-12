from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from neads.sequential_choices_model.i_step import IStep

if TYPE_CHECKING:
    from neads.activation_model import SealedActivationGraph, SealedActivation
    from neads.sequential_choices_model.tree_view import TreeView
    from neads.sequential_choices_model.choices_step.choice import Choice


class ChoicesStep(IStep):
    """Step which consist of sequence of choices.

    ChoicesStep is the classical, basic kind of step. It directly contain a
    sequence of choices, i.e. instances of Choice class.
    """

    def __init__(self):
        """Initialize empty ChoicesStep."""

        self.choices: list[Choice] = []

    def create(self, target_graph: SealedActivationGraph,
               parent_activation: SealedActivation,
               tree_view: TreeView,
               next_steps: Sequence[IStep]):
        """Add each choice to the graph and recursively adds the next steps.

        Each choice is added and serves as a base for nodes created by the
        next steps.

        Parameters
        ----------
        target_graph
            The graph to which will be the step's choices attached.
        parent_activation
            The Activation to which each choice is attached.
        tree_view
            The TreeView of the `target_graph`.
        next_steps
            The steps which are supposed to be created at the bottom of the
            part of the graph created by the step.

        Raises
        ------
        RuntimeError
            If the step has no choices.
        """

        # Error checking
        if len(self.choices) == 0:
            raise RuntimeError('ChoicesStep must have at least one choice.')

        # Creating the step's part of the graph
        step_results = []
        for choice in self.choices:
            result_act = choice.attach(target_graph, parent_activation)
            tree_view.add_child(parent_activation, result_act)
            step_results.append(result_act)
        # Invoking next steps to create their part of the graph
        self._create_next_steps(target_graph, step_results, tree_view,
                                next_steps)
