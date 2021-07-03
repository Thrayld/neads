from neads.activation_model import SealedActivationGraph, SealedActivation
from neads.sequential_choices_model.i_step import IStep


class ChoicesStep(IStep):
    """Step which consist of sequence of choices.

    ChoicesStep is the classical, basic kind of step. It directly contain a
    sequence of choices, i.e. instances of Choice class.
    """

    def __init__(self):
        """Initialize empty ChoicesStep."""

        raise NotImplementedError()
        # self.choices = []

    def create(self, target_graph: SealedActivationGraph,
               parent_activation: SealedActivation, tree_view,
               next_steps: list[IStep]):
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
        """

        raise NotImplementedError()
