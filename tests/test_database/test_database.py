from __future__ import annotations

import unittest

from typing import TYPE_CHECKING
import abc

from neads.database import IDatabase, DatabaseAccessError, DataNotFound



class BaseTestClassWrapper:
    """Excludes the BaseTestDatabase class from test suite.

    BaseTestDatabase is an abstract class not meant to be initialized
    directly. However, unittest module is careless of the fact.

    The solution is to move the class outside the module global scope.
    """

    class BaseTestDatabase(abc.ABC, unittest.TestCase):
        """Common test-class for tests of subclasses of IDatabase."""

        @abc.abstractmethod
        def get_database(self) -> IDatabase:
            pass

        def setUp(self):
            self.database: IDatabase = self.get_database()
            assert not self.database.is_open

        def tearDown(self) -> None:
            if self.database.is_open:
                self.database.close()

        def test_save_when_not_open(self):
            self.assertRaises(
                DatabaseAccessError,
                self.database.save,
                'data',
                'key'
            )

        def test_load_when_not_open(self):
            self.assertRaises(
                DatabaseAccessError,
                self.database.load,
                'key'
            )

        def test_close_when_not_open(self):
            self.assertRaises(
                DatabaseAccessError,
                self.database.close,
            )

        def test_open_when_opened(self):
            self.database.open()

            self.assertRaises(
                DatabaseAccessError,
                self.database.open,
            )

        def test_load_non_present_data(self):
            self.database.open()

            self.assertRaises(
                DataNotFound,
                self.database.load,
                'key'
            )

        def test_save_load(self):
            self.database.open()
            data, key = 'data', 'key'
            self.database.save(data, key)

            actual = self.database.load(key)

            self.assertEqual(data, actual)

        def test_open_close(self):
            self.assertFalse(self.database.is_open)
            self.database.open()
            self.assertTrue(self.database.is_open)
            self.database.close()
            self.assertFalse(self.database.is_open)

        def test_context_guard(self):
            self.assertFalse(self.database.is_open)
            with self.database:
                self.assertTrue(self.database.is_open)
            self.assertFalse(self.database.is_open)