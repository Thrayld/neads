from typing import Sequence, Optional

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

    def create_graph(self, data_presence: Optional[Sequence[bool]] = None) -> \
            SealedActivationGraph:
        """Create the graph described by the SCM.

        See class's docstring for more information.

        Parameters
        ----------
        data_presence
            Sequence of boolean values of length which equals the number of
            steps.
            For each step, it determines whether the result structure of the
            graph evaluation will contain data produced by result Activation
            of the step.
            In case None is provided, all data are preserved.

        Returns
        -------
            The graph described by the SCM. Its result of evaluation is an
            instance of ResultTree whose number of levels corresponds
            to the number of steps + 1 (each steps occupies one level and +1 is
            for the root).
        """

        raise NotImplementedError()
        # Page (2)
