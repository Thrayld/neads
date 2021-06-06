import unittest
import abc
import os

from neads.utilities.serializers.serializer import Serializer
from neads.utilities.serializers.pickle_serializer import PickleSerializer


class BaseTestClassWrapper:
    """Excludes the BaseTestSerializer class from test suite.

    BaseTestSerializes is an abstract class not meant to be initialized
    directly. However, unittest module is careless of the fact.

    The solution is to move the class outside the module global scope.
    """

    class BaseTestSerializer(abc.ABC, unittest.TestCase):
        """Common test-class for basic Serializer testing."""

        @abc.abstractmethod
        def get_serializer(self) -> Serializer:
            pass

        def setUp(self):
            self.filename = 'file_with_data'
            self.data = [1, '10', {}]

            self.serializer: Serializer = self.get_serializer()

        def tearDown(self) -> None:
            os.remove(self.filename)

        def test_save_load_with_existing_file(self):
            # Create file
            with open(self.filename, 'w') as f:
                pass

            self.serializer.save(self.data, self.filename)
            actual = self.serializer.load(self.filename)

            self.assertEqual(self.data, actual)

        def test_save_load_with_non_existing_file(self):
            self.serializer.save(self.data, self.filename)
            actual = self.serializer.load(self.filename)

            self.assertEqual(self.data, actual)

        def test_save_repeated_load(self):
            self.serializer.save(self.data, self.filename)

            actual_1 = self.serializer.load(self.filename)
            actual_2 = self.serializer.load(self.filename)
            actual_3 = self.serializer.load(self.filename)

            self.assertEqual(self.data, actual_1)
            self.assertEqual(self.data, actual_2)
            self.assertEqual(self.data, actual_3)


if __name__ == '__main__':
    unittest.main()
