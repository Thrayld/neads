from tests.test_evaluation_manager.test_single_thread_evaluation_manager \
    .test_evaluation_algorithms.test_evaluation_algorithm import \
    BaseTestClassWrapper
from neads.evaluation_manager.single_thread_evaluation_manager \
    .evaluation_algorithms import ComplexAlgorithm


class TestComplexAlgorithmWithoutSwapping(BaseTestClassWrapper.
                                          BaseTestEvaluationAlgorithm):

    def get_algorithm(self):
        return ComplexAlgorithm()


# TODO: Add more test with use of DB etc.
