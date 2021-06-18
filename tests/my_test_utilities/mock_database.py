from typing import Optional, Any

from neads.database import IDatabase, DataNotFound
from neads.activation_model import DataDefinition


class MockDatabase(IDatabase):

    def __init__(self, database_content: Optional[dict[DataDefinition, Any]]):
        if database_content is None:
            database_content = {}
        self._content = database_content

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def save(self, data, data_def):
        self._content[data_def] = data

    def load(self, data_def):
        try:
            return self._content[data_def]
        except KeyError as e:
            raise DataNotFound() from e