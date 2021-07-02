import pathlib

from neads.database import IDatabase, DataNotFound


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

        pass

    def __init__(self, dir_name):
        """Initializes a FileDatabase.

        The directory must exist and contain all necessary. Use `create`
        method to create an empty Database in the file first.

        Parameters
        ----------
        dir_name
            Directory with a FileDatabase.
        """

        pass

    @property
    def is_open(self):
        """Whether the database is open."""
        pass

    def _do_open(self):
        """Do open the database."""
        pass

    def _do_close(self):
        """Do close the database."""
        pass

    def _do_save(self, data, key):
        """Do save the given data under the given key.

        Parameters
        ----------
        data
            The data to save to the database.
        key
            The key for the data.
        """

        pass

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
