import tempfile
import weakref


from serializers.serializer import Serializer
from serializers.pickle_serializer import PickleSerializer


def _get_tmp_path():
    """Generates a path for temporary file using tempfile library.

    The method is actually quite slow, but also very safe (e.g. thread safe).

    The algorithm calls tempfile.mkstemp(), CLOSES the file and then return
    its name. Thus, the file is created and closed.

    Returns
    -------
        Path for temporary file.
    """

    # descriptor_int, path = tempfile.mkstemp()
    raise NotImplementedError()


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

    # PATH_GENERATOR = _get_tmp_path()

    def __init__(self, *, path=None,
                 serializer: Serializer = PickleSerializer()):
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

        raise NotImplementedError()

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

        raise NotImplementedError()

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

        raise NotImplementedError()

    def dispose(self):
        """Dispose the TempFile object.

        The the disk space will be freed.
        """

        raise NotImplementedError()
