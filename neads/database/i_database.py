import abc


class DataNotFound(Exception):
    pass


class DatabaseAccessError(Exception):
    pass


class IDatabase(abc.ABC):
    """General interface for Database with implemented basic error checking."""

    @property
    @abc.abstractmethod
    def is_open(self):
        """Whether the database is open."""
        pass

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def open(self):
        """Open the database, i.e. prepare it for use.

        Raises
        ------
        DatabaseAccessError
            If the database is not closed (reopening signals logical error in
            the user's code).
        """

        if self.is_open:
            raise DatabaseAccessError('The database must be closed when '
                                      'opening.')
        self._do_open()

    def close(self):
        """Close the database, i.e. end the use.

        Raises
        ------
        DatabaseAccessError
            If the database is not open (closing a closed database signals
            logical error in the user's code).
        """

        self._assert_database_is_open('The database must be open when closing.')
        self._do_close()

    def save(self, data, key):
        """Save the given data under the given key.

        Parameters
        ----------
        data
            The data to save to the database.
        key
            The key for the data.

        Raises
        ------
        DatabaseAccessError
            If the database is not open.
        """

        self._assert_database_is_open('The database must be open when saving '
                                      'data.')
        self._do_save(data, key)

    def load(self, key):
        """Load data under the given key from the database.

        Parameters
        ----------
        key
            The key for the data.

        Returns
        -------
            The data corresponding to the key.

        Raises
        ------
        DatabaseAccessError
            If the database is not open.
        DataNotFound
            If there are no data for the given key in the database.
        """

        self._assert_database_is_open('The database must be open when loading '
                                      'data.')
        return self._do_load(key)

    @abc.abstractmethod
    def _do_open(self):
        """Do open the database."""
        pass

    @abc.abstractmethod
    def _do_close(self):
        """Do close the database."""
        pass

    @abc.abstractmethod
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

    @abc.abstractmethod
    def _do_load(self, key):
        """Do load data under the given data_definition key from the database.

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

    def _assert_database_is_open(self, msg=''):
        """Check that the database is open, raise exception if not.

        Raises
        ------
        DatabaseAccessError
            If the database is not open.
        """

        if not self.is_open:
            raise DatabaseAccessError(msg)
