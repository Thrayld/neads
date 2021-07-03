import unittest


from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_manager import SingleThreadEvaluationManager
from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_algorithms import TopologicalOrderAlgorithm

from tests.my_test_utilities.mock_database import MockDatabase
import tests.my_test_utilities.activation_graphs_for_tests as graphs


# TODO: Write true unit tests

class TestEvaluationManager(unittest.TestCase):
    def setUp(self) -> None:
        self.db = MockDatabase()
        self.em = SingleThreadEvaluationManager(self.db)

    def test_evaluate_with_given_algorithm(self):
        graph, results = graphs.trigger_on_result_with_graph_trigger()
        alg = TopologicalOrderAlgorithm()

        actual = self.em.evaluate(graph, alg)

        self.assertDictEqual(results, actual)

    def test_evaluate_with_default_algorithm(self):
        graph, results = graphs.trigger_on_result_with_graph_trigger()

        actual = self.em.evaluate(graph)

        self.assertDictEqual(results, actual)


if __name__ == '__main__':
    unittest.main()
