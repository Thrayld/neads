from typing import TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation


class State(Enum):
    """State of the DataNode."""

    UNKNOWN = auto()
    NO_DATA = auto()
    MEMORY = auto()
    DISK = auto()


class DataNode:
    """Node in EvaluationState for a single Activation in ActivationGraph.

    DataNode represents data of a single Activation. It is in one of the
    following states: UNKNOWN, NO_DATA, MEMORY, DISK. These states are
    represented by the values of enum State.

    In UNKNOWN state, we do not know yet, whether we already have the data or
    not. We need to check it first (to database, if there is any) via method
    try_load().

    In NO_DATA state, we know that we do not have the data. If the user wants
    them, they must be computed via evaluate() method.

    In MEMORY state, the node data are in memory. If it is necessary to release
    some memory, the data may be moved to disk via store() method.

    In DISK state, the data are on disk. If they need to become active
    (usually because a child of the node is meant to be evaluated), the data
    may be moved to memory via load() method.

    For more detail on the methods, see their docstring.
    """

    # TODO: provide public handlers (is that the word?) that allow anybody
    #  (EvaluationState in our case) to attach its own handler that will react
    #  on change of state

    def __init__(self, activation: SealedActivation):
        """Initialize a DataNode instance.

        Parameters
        ----------
        activation
            The Activation whose data and state the DataNode instance
            represents.
        """

        raise NotImplementedError()

    @property
    def state(self):
        """State of the DataNode."""
        raise NotImplementedError()

    @property
    def parents(self):
        """Parent nodes of the DataNode.

        The relations child-parent corresponds to the underlying
        ActivationGraph.
        """
        raise NotImplementedError()

    @property
    def children(self):
        """Child nodes of the DataNode.

        The relations child-parent corresponds to the underlying
        ActivationGraph.
        """
        raise NotImplementedError()

    @property
    def has_trigger_on_result(self):
        """Whether the corresponding Activation has trigger-on_result."""
        raise NotImplementedError()

    @property
    def has_trigger_on_descendants(self):
        """Whether the corresponding Activation has trigger-on-descendants."""
        raise NotImplementedError()

    @property
    def data_size(self):
        """Size of the actual data in bytes, if it is known.

        The size is not known in UNKNOWN and NO_DATA state and None is returned.
        Also note that in DISK state the size is known, but the data of such
        size are not in memory but only on disk (more precisely, it depends
        on the behavior of GC).
        """
        raise NotImplementedError()

    def try_load(self) -> bool:
        """Try load the data from database.

        Allowed only in UNKNOWN state. There are two possible results. Either
        the attempt to load the data was successful and the state changes to
        MEMORY. Or, in case the attempt was not successful, the state changes
        to NO_DATA.

        Returns
        -------
            True, it the attempt to load was successful. False otherwise.
        """

    def evaluate(self):
        """Evaluate the data.

        Allowed only in NO_DATA state and the resulting state is MEMORY.
        The method calls the corresponding plugin with appropriate arguments.
        The parent nodes MUST be in MEMORY state when calling evaluate().

        Raises
        ------
        TODO exception
            A parent node was not in MEMORY state.
        TODO
            general exception for calling the method while being in wrong state
        """

    def store(self):
        """Store data on disk.

        Allowed only in MEMORY state and the resulting state is DISK. It stores
        the data to tmp file and releases the pointer to the data instance.

        TODO: how much entanglement is there between data instances in
         usual case?
         Is there any?
         Will we really release as much memory as promised (after run of GC)
        """

    def load(self):
        """Load data to memory.

        Allowed only in DISK state and the resulting state is MEMORY. Data
        are loaded from tmp file to memory.
        """
