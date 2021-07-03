from neads.activation_model import SealedActivationGraph


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

    def create_graph(self) -> SealedActivationGraph:
        """Create the graph described by the SCM.

        See class's docstring for more information.

        Returns
        -------
            The graph described by the SCM.
        """

        raise NotImplementedError()
        # Page (2)
