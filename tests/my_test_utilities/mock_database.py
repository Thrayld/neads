from typing import Optional, Any

from neads.database import IDatabase, DataNotFound
from neads.activation_model import DataDefinition


class MockDatabase(IDatabase):

    @property
    def is_open(self):
        return self._is_open

    def _do_open(self):
        self._is_open = True

    def _do_close(self):
        self._is_open = False

    def _do_save(self, data, key):
        self._content[key] = data

    def _do_load(self, key):
        try:
            return self._content[key]
        except KeyError as e:
            raise DataNotFound() from e

    def __init__(self,
                 database_content: Optional[dict[DataDefinition, Any]] = None):
        self._is_open = False
        if database_content is None:
            database_content = {}
        self._content = database_content
