from tests.test_database.test_database import BaseTestClassWrapper
from tests.my_test_utilities.mock_database import MockDatabase


class TestMockDatabase(BaseTestClassWrapper.BaseTestDatabase):

    def get_database(self):
        return MockDatabase()
