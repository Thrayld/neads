from typing import TYPE_CHECKING, Any, Optional
import os
import pathlib
import pickle as pkl

from neads.database import IDatabase, DataNotFound
from neads._internal_utils.serializers import PickleSerializer

if TYPE_CHECKING:
    from neads._internal_utils.serializers import ISerializer


# TODO: Add 'destroy' method and add optional param 'create' to __init__

class FileDatabase(IDatabase):
    """Database which saves each data instance to its own file via serializer.

    In addition, the database manages an index dictionary which maps the keys
    to the files containing their data. The dictionary is serializer using
    pickle.
    """

    INDEX_FILENAME = 'index'
    DATA_DIR = 'data'

    @staticmethod
    def create(dir_name):
        """Create an empty FileDatabase in the given directory.

        Parameters
        ----------
        dir_name
            Directory where to create the database. The path must not exist.
        """

        db_path = pathlib.Path(dir_name)
        # Creating DB's dir
        os.mkdir(db_path)
        # Creating empty index
        with open(db_path / FileDatabase.INDEX_FILENAME, 'wb') as f:
            pkl.dump({}, f)
        # Creating dir for data
        os.mkdir(db_path / FileDatabase.DATA_DIR)

    def __init__(self, dir_name, *, serializer=None):
        """Initializes a FileDatabase.

        The directory must exist and contain all necessary. Use `create`
        method to create an empty Database in the file first.

        Parameters
        ----------
        dir_name
            Directory with a FileDatabase.
        """

        db_path = pathlib.Path(dir_name)
        self._index_path = db_path / self.INDEX_FILENAME
        self._data_dir_path = db_path / self.DATA_DIR

        self._is_open = False
        # The filenames are ints for memory savings
        self._index: Optional[dict[Any, int]] = None
        # Serializer for the actual data (index is always by pickle)
        self._serializer: ISerializer = serializer \
            if serializer is not None \
            else PickleSerializer()

    @property
    def is_open(self):
        """Whether the database is open."""
        return self._is_open

    def _do_open(self):
        """Do open the database."""
        with open(self._index_path, 'rb') as f:
            self._index = pkl.load(f)
        self._is_open = True

    def _do_close(self):
        """Do close the database."""
        self._is_open = False
        with open(self._index_path, 'wb') as f:
            pkl.dump(self._index, f)

    def _do_save(self, data, key):
        """Do save the given data under the given key.

        Parameters
        ----------
        data
            The data to save to the database.
        key
            The key for the data.
        """

        # Try if the key already exists
        try:
            data_path = self._get_path_for_key(key)
        except DataNotFound:
            # We need to generate new file
            data_path = self._add_new_file_name(key)
        self._serializer.save(data, data_path)

    def _do_load(self, key):
        """Do load data under the given key from the database.

        Parameters
        ----------
        key
            The key for the data.

        Returns
        -------
            The data corresponding to the key.

        Raises
        ------
        DataNotFound
            If there are no data for the given key in the database.
        """

        data_path = self._get_path_for_key(key)
        return self._serializer.load(data_path)

    def _do_delete(self, key):
        """Do delete data under the given key from the database.

        Parameters
        ----------
        key
            The key for the data.

        Raises
        ------
        DataNotFound
            If there are no data for the given key in the database.
        """

        data_path = self._get_path_for_key(key)
        os.remove(data_path)
        del self._index[key]

    def _get_path_for_key(self, key):
        """Return path to file with data corresponding to the given key.

        Parameters
        ----------
        key
            Key whose corresponding data file is returned.

        Returns
        -------
            Path to file with data corresponding to the given key.

        Raises
        ------
        DataNotFound
            If there are no data for the given key in the database.
        """

        if (file_number := self._index.get(key, None)) is not None:
            data_path = self._data_dir_path / str(file_number)
            return data_path
        else:
            raise DataNotFound(f'The are no data for the given key: {key}')

    def _add_new_file_name(self, key):
        """Generate new file name and add it to index under the given key.

        Parameters
        ----------
        key
            Key for the new filename.

        Returns
        -------
            Path to the new file.
        """

        # We are using the fact that dict keep the insertion order
        # And the fact that are values always grow, so the last dict's value
        # is the largest value of all

        if self._index:
            largest_used_value = next(reversed(self._index.values()))
        else:
            largest_used_value = -1  # We start from 0

        new_file_number = largest_used_value + 1
        new_file_path = self._data_dir_path / str(new_file_number)
        self._index[key] = new_file_number
        return new_file_path
