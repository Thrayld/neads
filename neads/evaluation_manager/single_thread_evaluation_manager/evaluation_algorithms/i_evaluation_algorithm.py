from __future__ import annotations

from typing import TYPE_CHECKING, Any
import abc

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation
    from neads.evaluation_manager.single_thread_evaluation_manager \
        .evaluation_state import EvaluationState


class IEvaluationAlgorithm(abc.ABC):
    """General interface for EvaluationAlgorithms."""

    @abc.abstractmethod
    def evaluate(self, evaluation_state: EvaluationState) \
            -> dict[SealedActivation, Any]:
        """Alter the evaluation state to evaluate the underlying graph.

        The evaluation has two steps.
        First, the algorithm must evaluate all 'objective nodes' (property of
        ES), more precisely gets them to MEMORY state (either by evaluation or
        load from database).
        Then, the algorithm must get data from all 'result nodes' which are
        then returned.

        TODO: find way to get activation from the DataNode.. maybe let ES
         to return the result 'structure' (i.e. the dict Act to Data)
         ale to se mi moc nelibi, proc do toho takhle zatahovat ES, lepsi DN,
         kdyz uz jsme dosli ke get_data

        Parameters
        ----------
        evaluation_state
            Instance of evaluation state, whose graph is evaluated.

        Returns
        -------
            Dictionary which maps childless Activations of the graph to their
            results.
        """

        raise NotImplementedError()
