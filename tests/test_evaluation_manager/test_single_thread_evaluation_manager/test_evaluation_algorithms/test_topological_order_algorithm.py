from tests.test_evaluation_manager.test_single_thread_evaluation_manager \
    .test_evaluation_algorithms.test_evaluation_algorithm import \
    BaseTestClassWrapper
from neads.evaluation_manager.single_thread_evaluation_manager \
    .evaluation_algorithms import TopologicalOrderAlgorithm


class TestTopologicalOrderAlgorithm(BaseTestClassWrapper.
                                    BaseTestEvaluationAlgorithm):
    """Tests serializer based on the pickle protocol."""

    def get_algorithm(self):
        return TopologicalOrderAlgorithm()
