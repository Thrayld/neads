from __future__ import annotations

from typing import TYPE_CHECKING

from neads.activation_model import SealedActivationGraph, SealedActivation
from neads.sequential_choices_model.i_step import IStep


class DynamicStep(IStep):
    """Step which creates choices dynamically by the partial evaluation results.

    The DynamicStep creates a several parametrized choices (by index) in
    shape of the so-called extractor whose count is determined dynamically by
    the result of a part of graph called the separator.

    The separator is an ActivationGraph with one input which and has one result
    Activation. It is attached to the graph first. Then, the length of the
    Activation's data (truly computed by the len() function) determines how
    many times the extractor will be attached to the graph.

    The extractor is an ActivationGraph with 3 inputs, the first for the data
    of the Activation which served as input to the separator (i.e. the
    `parent_activation` in create method), the second for data of separator
    and the last for index to the data. The extractor has, as usual,
    one result Activation which is considered to be the result of step's
    choice. That is, step's choices results are the result Activation of
    attached extractors (i.e. they are added as children of the
    `parent_activation` to the TreeView and the next steps are attached to
    them).

    The creation of the extractors naturally happens in a trigger-on-result
    of separator's result Activation. It also subsequently creates the next
    steps.

    Examples
    --------
        Suppose we have a network and we to run a clustering algorithm on
        it and the perform an analysis of each cluster. We do not know (for
        some algorithms) have many clusters will be found. Thus, we cannot
        use the simple ChoicesStep.

        We use the DynamicStep as follows. As the separator we set a graph
        with a single Activation with the plugin which computes the clustering.
        The clustering will be represented by a list of clusters such that each
        cluster is described by a list of its nodes.

        The extractor is again a graph with a single Activation. It takes
        three arguments, the first is the original network (data of
        separator's parent), the second is the list of all clusters (data
        of separator) and the last is the index, which differs for each
        realization of the extractor. The simple job of the extractor's
        plugin is to take a subnetwork of the original one containing exactly
        those nodes given by the appropriate cluster (from separator's data)
        given by the index.

        Then, in the next step we can start with an analysis of each cluster.
    """

    def __init__(self, separator: Separator, extractor: Extractor):
        """Initialize DynamicStep.

        See class's docstring for more info.

        Parameters
        ----------
        separator
            Separator of the DynamicStep.
        extractor
            Extractor of the DynamicStep.
        """

        raise NotImplementedError()

    def create(self, target_graph: SealedActivationGraph,
               parent_activation: SealedActivation, tree_view,
               next_steps: list[IStep]):
        """Add the separator to the graph and leave the rest for its trigger.

        See class's docstring for more info.

        Parameters
        ----------
        target_graph
            The graph to which will the separator and later the extractors
            (choices) attached.
        parent_activation
            The Activation to which the separator and each extractor is
            attached.
        tree_view
            The TreeView of the `target_graph`.
        next_steps
            The steps which are supposed to be created at the bottom of the
            part of the graph created by the step.
        """

        raise NotImplementedError()
