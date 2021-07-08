import os
import tempfile
import weakref


from neads._internal_utils.serializers.i_iserializer import ISerializer
from neads._internal_utils.serializers.pickle_serializer import PickleSerializer


# TODO: Add IObjectTempFileProvider class which will create IObjectTempFile
#  - easier mocking (which is very much desirable)
#  - avoiding share state `PATH_GENERATOR`

def _get_temp_path():
    """Generates a path for temporary file using tempfile library.

    The method is actually quite slow, but also very safe (e.g. thread safe).

    The algorithm guarantees creation of a unique name by calling
    tempfile.mkstemp(), CLOSING the file and returning its name. Thus,
    the file is created and closed, but also the caller can be sure that no
    race condition when occupying the path.

    Nota that the file with the path is created and is supposed to be
    removed by the caller!

    Returns
    -------
        Unique path for temporary file with 'neads_' prefix.
    """

    descriptor_num, path = tempfile.mkstemp(prefix='neads_')
    os.close(descriptor_num)
    return path


def _remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


class ObjectTempFile:
    """Simple temp-file for loading and storing objects via custom serializer.

    The ObjectTempFile supports 2 operations - store and load an object.
    Also, it the ObjectTempFile can be removed manually by `dispose` method.
    After calling the method, the ObjectTempFile can't be used again.

    The clean-up method is called when the first of the following events occurs:

    * the ObjectTempFile is garbage collected,

    * the ObjectTempFile’s dispose() method is called, or

    * the program exits.

    Thus, it is very reliable that the disk resources are released if no
    longer needed (unlike with __del__ statement in some Python
    implementations).
    """

    PATH_GENERATOR = _get_temp_path

    def __init__(self, *, path=None,
                 serializer: ISerializer = PickleSerializer()):
        """Create new TempFile instance.

        Parameters
        ----------
        path
            Path to the file, if the user wants to control the location of
            the file.

            By default, the name is generated via PATH_GENERATOR. See its
            documentation for more information.

        serializer
            Serializer used for converting the Python object to a format in
            which the object is stored. Also, for inverse conversion in load
            method.

            By default, PickleSerializer is used.
        """

        self._path = path if path is not None else type(self).PATH_GENERATOR()
        self._serializer = serializer
        self._finalizer = weakref.finalize(self, _remove_if_exists, self._path)
        self._is_object_present = False

    def load(self):
        """Load the object from the the file.

        The file is suppose to survive the load, so a repeated load is possible.

        Returns
        -------
            The deserialized object from the file.

        Raises
        ------
        RuntimeError
            Attempt to load data before saving them.
            Attempt to access disposed object.
        """

        if not self.is_disposed:
            if self._is_object_present:
                return self._serializer.load(self._path)
            else:
                raise RuntimeError(f'Cannot load from file without object.')
        else:
            raise RuntimeError(f'The file at {self._path} were disposed.')

    def save(self, obj):
        """Save the object to the the file.

        Parameters
        ----------
        obj
            Object to save in the file.

        Raises
        ------
        RuntimeError
            Attempt to access disposed object.
        """

        if not self.is_disposed:
            self._serializer.save(obj, self._path)
            self._is_object_present = True
        else:
            raise RuntimeError(f'The file at {self._path} were disposed.')

    def dispose(self):
        """Dispose the TempFile object.

        The the disk space will be freed.
        """

        self._finalizer()

    @property
    def is_disposed(self):
        """Whether the object was already disposed."""

        return not self._finalizer.alive
