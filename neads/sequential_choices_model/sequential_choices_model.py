from typing import Iterable, Optional

from neads.activation_model import SealedActivationGraph

# IDEA: Complete the SCM's API and polish it


class SequentialChoicesModel:
    """Class providing user simple creation of complex SealedActivationGraphs.

    SequentialChoicesModel, as the name suggest, views the computation as a
    sequence of steps, each with several choices, i.e. ways to perform the step.
    So-called DynamicSteps, whose number of choices is determined dynamically,
    are also possible.

    The results are exactly the sequences of choices such that we take one
    choice for each step. All the results are then brought to a single node
    whose result data structure gather results of all choices of selected steps
    and provide query mechanism.
    """

    def __init__(self):
        """Initialize empty SequentialChoicesModel."""

        raise NotImplementedError()
        # self.steps: IStep = []

    def create_graph(self, data_presence: Optional[Iterable[int]] = None) -> \
            SealedActivationGraph:
        """Create the graph described by the SCM.

        See class's docstring for more information.

        Parameters
        ----------
        data_presence
            Set of integers to determine the steps whose data will appear in
            the graph's result structure (after evaluation via
            EvaluationManager).
            That is, for each step, the result structure of the graph evaluation
            will contain data produced by result Activations of the step,
            if the `data_presence` iterable contain the step's index in the
            `self.steps` list.
            In case None is provided (default), the data of all steps are
            preserved.

        Returns
        -------
            The graph described by the SCM. After all trigger invocations,
            it has single result Activation whose produces data (SCM's result
            structure) is an instance of ResultTree whose number of levels
            corresponds to the number of steps + 1 (each steps occupies one
            level and +1 is for the root).

        Raises
        ------
        ValueError
            If the `data_presence` argument contains invalid index,
            i.e. a value which is less than 0 or equal to or greater than
            the length of the `self.steps` list.
        """

        raise NotImplementedError()
        # Page (2)
