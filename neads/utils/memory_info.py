"""Provide info about process and object memory usage."""

# The module is not hidden behind an interface, because in case we changed the
# implementation, we are very likely to change the contract as well (e.g.
# provide more specific information than process usage). Thus, the interface
# would make no difference.

from pympler.asizeof import asizeof


def get_process_usage():
    """Return number of bytes used by the running process.

    The number is obtained directly from OS. Note that its changes
    depends heavily on the running Python implementation and its memory
    management policy.

    Returns
    -------
        Number of bytes used by the running process.
    """

    pass


def get_object_usage(obj):
    """Return number of bytes used by the given object.

    The consumption is computed recursively. The size of repeatedly visited
    referents is counted only once.

    Note that some of the subobjects may not be referenced exclusively by
    the given object. Thus, deletion of the given object may not result
    in deletion of all its subobjects.

    Parameters
    ----------
    obj
        Object, whose memory consumption is returned.

    Returns
    -------
        Number of bytes used by the given object.
    """

    pass
