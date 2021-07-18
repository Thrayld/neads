from typing import TYPE_CHECKING, Iterable, Optional

from neads.activation_model import SealedActivationGraph
from neads.sequential_choices_model.tree_view import TreeView
from neads.sequential_choices_model.scm_plugins import root_plugin, \
    result_plugin
from neads import ListObject, DictObject, Value
from neads.activation_model.symbolic_objects.symbolic_object import \
    SymbolicObject


if TYPE_CHECKING:
    from neads.sequential_choices_model.i_step import IStep

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

        self.steps: list[IStep] = []

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
            present.

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
        RuntimeError
            If the SCM instance is without steps.
        """

        # Error checking
        # All valid indices
        if data_presence is not None:
            sorted_indices = sorted(list(data_presence))
            if sorted_indices[0] < 0 or sorted_indices[-1] >= len(self.steps):
                raise ValueError(
                    f"Invalid range of 'data_presence' indices: {data_presence}"
                )
        else:
            data_presence = range(len(self.steps))
        # Presence of steps
        if len(self.steps) == 0:
            raise RuntimeError(
                'SequentialChoicesModel must have at least one choice.'
            )

        # Create some initial objects
        present_steps_indices = set(data_presence)
        scm_graph = SealedActivationGraph()
        root_activation = scm_graph.add_activation(root_plugin)
        tree_view = TreeView(root_activation)
        first_step, next_steps = self.steps[0], self.steps[1:]

        # Let the steps build the graph
        first_step.create(scm_graph, root_activation, tree_view, next_steps)

        # Assign graph's trigger, which one day create the result Activation
        scm_graph.trigger_method = self._get_graph_trigger(
            scm_graph, tree_view, present_steps_indices)

        return scm_graph

    def _get_graph_trigger(self, scm_graph, tree_view, present_steps_indices):
        """Return trigger method for the SCM's graph.

        Parameters
        ----------
        scm_graph
            The created scm_graph.
        tree_view
            The tree view used for capturing tree structure of the SCM's graph.
        present_steps_indices
            Iterable of indices of the present steps in the result structure.

        Returns
        -------
            Trigger method for the SCM's graph which creates one
            result Activation. The Activation collects the demanded results
            are puts them in result structure.
        """

        # TreeView regards the 0 index as root's index
        # The indices for steps start from 1
        altered_indices = set(idx + 1 for idx in present_steps_indices)

        def trigger():
            description = tree_view.get_result_description(altered_indices)
            # Create SymbolicObject description
            actual_description = self._create_symbolic_object_description(
                description)
            result_act = scm_graph.add_activation(result_plugin,
                                                  actual_description)
            # Return the created Activations - the result Activation
            return [result_act]

        return trigger

    @staticmethod
    def _create_symbolic_object_description(old_description):
        """Transform list of dicts to corresponding SymbolicObject

        Parameters
        ----------
        old_description
            List of dict.

        Returns
        -------
            ListObject of the respective DictObject.
        """

        # Create DictObjects
        dict_objects = []
        for dict_ in old_description:
            new_dict = {}
            for key, val in dict_.items():
                # Transform to SymbolicObjects
                new_dict[Value(key)] = val \
                    if isinstance(val, SymbolicObject) \
                    else Value(val)
            dict_objects.append(DictObject(new_dict))
        # Create and return the resulting ListObject
        sym_object = ListObject(*dict_objects)
        return sym_object
