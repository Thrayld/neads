import unittest

from typing import TYPE_CHECKING, Callable, Any
import abc

from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_state import EvaluationState

import tests.my_test_utilities.activation_graphs_for_tests as graphs
from tests.my_test_utilities.mock_database import MockDatabase

if TYPE_CHECKING:
    from neads.evaluation_manager.single_thread_evaluation_manager \
        .evaluation_algorithms import IEvaluationAlgorithm
    from neads.activation_model import SealedActivation, SealedActivationGraph


class BaseTestClassWrapper:
    """Excludes the BaseTestEvaluationAlgorithm class from test suite.

    BaseTestEvaluationAlgorithm is an abstract class not meant to be
    initialized directly. However, unittest module is careless of the fact.

    The solution is to move the class outside the module global scope.
    """

    class BaseTestEvaluationAlgorithm(abc.ABC, unittest.TestCase):
        """Common test-class for tests of EvaluationAlgorithm."""

        @abc.abstractmethod
        def get_algorithm(self) -> IEvaluationAlgorithm:
            pass

        @staticmethod
        def get_evaluation_state(activation_graph):
            db = MockDatabase()
            es = EvaluationState(activation_graph, db)
            return es

        def assertGraphResultsEqual(self, expected_results, graph, msg=None):
            es = self.get_evaluation_state(graph)

            actual_results = self.algorithm.evaluate(es)

            self.assertDictEqual(expected_results, actual_results, msg)

        def test_graph_generator(
                self,
                graph_generator: Callable[
                    [],
                    tuple[SealedActivationGraph, dict[SealedActivation, Any]]
                ]
        ):
            graph, expected_results = graph_generator()
            self.assertGraphResultsEqual(expected_results, graph)

        def setUp(self):
            self.algorithm: IEvaluationAlgorithm = self.get_algorithm()

        def test_simple_tree(self):
            self.test_graph_generator(graphs.simple_tree)

        def test_simple_diamond(self):
            self.test_graph_generator(graphs.simple_diamond)

        def test_simple_trigger_on_result(self):
            self.test_graph_generator(graphs.simple_trigger_on_result)

        def test_trigger_on_result_with_graph_trigger(self):
            self.test_graph_generator(
                graphs.trigger_on_result_with_graph_trigger)
