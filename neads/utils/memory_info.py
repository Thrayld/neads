"""Provide info about process and object memory usage."""

# The module is not hidden behind an interface, because in case we changed the
# implementation, we are very likely to change the contract as well (e.g.
# provide more specific information than process usage). Thus, the interface
# would make no difference.

import pympler.asizeof
import psutil


def get_process_virtual_memory():
    """Return total amount of virtual memory used by the process.

    The value is obtained as VMS of the running process via `psutil`.

    Returns
    -------
        Total amount of virtual memory used by the process. The number is in
        bytes.
    """

    process = psutil.Process()
    return process.memory_info().vms


def get_process_ram_memory():
    """Return size of non-swapped physical memory used by the process.

    The value is obtained as RSS of the running process via `psutil`.

    Returns
    -------
        Size in bytes of non-swapped physical memory used by the process.
    """

    process = psutil.Process()
    return process.memory_info().rss


def get_available_memory():
    """Return the available physical memory.

    The value is obtained as available virtual memory of the running process
    via `psutil`. It is the memory that can be given instantly to processes
    without the system going into swap.

    Returns
    -------
        Size in bytes of the available physical memory.
    """

    return psutil.virtual_memory().available


def get_object_size(obj):
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

    return pympler.asizeof.asizeof(obj)
