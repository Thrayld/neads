from typing import Any, Union
import os
import abc

PathLike = Union[str, bytes, os.PathLike]


class ISerializer(abc.ABC):
    """Interface for a serializer class."""

    @abc.abstractmethod
    def save(self, data: Any, filename: PathLike):
        """Save data into a file with the given name.

        Parameters
        ----------
        data
            Data to save to the file.
        filename
            Name of the file where the data will be saved. The file does
            not need to exist.
        """

        pass

    @abc.abstractmethod
    def load(self, filename: PathLike) -> Any:
        """Load and return data from a file with the given name.

        The file is suppose to survive the load, so a repeated load is possible.

        Parameters
        ----------
        filename
            Name of the file from which the data will be loaded.

        Returns
        -------
        Any
            Loaded data, ie. content of the file.
        """

        pass
