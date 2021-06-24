import unittest
import unittest.mock as mock

from neads.activation_model import SealedActivationGraph
from neads.evaluation_manager.single_thread_evaluation_manager\
    .evaluation_state import EvaluationState

import tests.my_test_utilities.arithmetic_plugins as ar_plugins
from tests.my_test_utilities.mock_database import MockDatabase


class TestEvaluationStateMemoryMethods(unittest.TestCase):
    def setUp(self):
        mock_path = 'neads.evaluation_manager' \
                    '.single_thread_evaluation_manager' \
                    '.evaluation_state' \
                    '.memory_info'
        self.patcher = mock.patch(mock_path)
        self.memory_info_mock = self.patcher.start()

        self.vms = 1
        self.rss = 2
        self.av_mem = 3

        self.memory_info_mock.get_process_virtual_memory.return_value = self.vms
        self.memory_info_mock.get_process_ram_memory.return_value = self.rss
        self.memory_info_mock.get_available_memory = self.av_mem

        ag = SealedActivationGraph()
        ag.add_activation(ar_plugins.const, 10)

        self.es = EvaluationState(ag, MockDatabase())

    def tearDown(self):
        self.patcher.stop()

    def test_used_virtual_memory(self):
        self.assertEqual(self.vms, self.es.used_virtual_memory)

    def test_used_physical_memory(self):
        self.assertEqual(self.rss, self.es.used_physical_memory)

    def test_available_memory(self):
        self.assertEqual(self.av_mem, self.es.available_memory)


if __name__ == '__main__':
    unittest.main()
