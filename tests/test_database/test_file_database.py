from tests.test_database.test_database import BaseTestClassWrapper

import tests.my_test_utilities.empty_file_database as file_db


class TestFileDatabase(BaseTestClassWrapper.BaseTestDatabase):

    def get_database(self):
        return file_db.get()

    def tearDown(self) -> None:
        super().tearDown()
        file_db.delete()
