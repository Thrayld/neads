from __future__ import annotations

from typing import TYPE_CHECKING, Iterable
import inspect

if TYPE_CHECKING:
    from .symbolic_objects import Symbol


class SymbolicArgumentSet:
    """Capture symbolic arguments of a function with given signature.

    Arguments for the function are SymbolicObjects which describes the shape
    of the actual arguments. The SymbolicArgumentSet allows substitution for
    the Symbols (any Symbol in the SymbolicObjects) to get the real
    arguments, with which the function may be called.

    The SymbolicArgumentSet is immutable, therefore any substitution produces
    a new instance of SymbolicArgumentSet, instead of modifying the original
    one.
    """

    def __init__(self, signature: inspect.Signature, /, *args, **kwargs):
        """Initialize SymbolicArgumentSet instance.

        The signature of a function is passed as the first argument followed
        by the actual arguments for the function. Some of them might be
        instances of SymbolicObject.

        Parameters
        ----------
        signature
            Signature of the function whose arguments are passed later.
        args
            Positional arguments for the function whose signature is passed.
        kwargs
            Keyword arguments for the function whose signature is passed.
        """

    def get_symbols(self) -> Iterable[Symbol]:
        """Return an iterable of Symbols occurring in argument's SymbolicObject.

        Returns
        -------
            An iterable of all Symbols which occur is at least of the symbolic
            arguments.
        """

    def substitute(self, *args) -> SymbolicArgumentSet:
        """Substitute SymbolicObjects for Symbols in `self`.

        If a replacement occurs, new SymbolicArgumentSet is created from `self`,
        because SymbolicArgumentSet is immutable.

        Parameters
        ----------
        args
            One of the following:

            * Two arguments `symbol_from` and `object_to`.

            * Iterable with the pairs `symbol_from`, `object_to`.

            * Dict with `symbol_from` as keys and `object_to` as values.

        Returns
        -------
            SymbolicArgumentSet after substitution.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        ValueError
            If 0 or more than 2 arguments are passed, or one `symbol_from`
            occurs multiple times.
        """

    def get_actual_arguments(self, *args, copy=True) -> inspect.BoundArguments:
        """Return the actual arguments described by SymbolicArgumentSet.

        If there are Symbols (i.e. free variables) in the SymbolicObject,
        they must be replaced by some objects. Unlike in the `substitute`
        method, here the objects are not required to be instances of
        SymbolicObject.

        Parameters
        ----------
        args
            One of the following:

            * Two arguments `symbol_from` and `object_to`.

            * Iterable with the pairs `symbol_from`, `object_to`.

            * Dict with `symbol_from` as keys and `object_to` as values.
        copy
            Whether a deep copy of given objects should appear in the
            resulting arguments.

            It is safer to create the copy to prevent intertwining between
            the original objects and the objects in the arguments. The
            modification of non-copied objects may result in unexpected
            behavior.

        Returns
        -------
            The actual bound arguments which the SymbolicArgumentSet describes.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        ValueError
            If 0 or more than 2 arguments are passed, or one `symbol_from`
            occurs multiple times.
        SymbolicObjectException
            If there are some unsubstituted Symbols left in the
            SymbolicArgumentSet.
        """

    def __eq__(self, other: SymbolicArgumentSet) -> bool:
        """Compare the SymbolicArgumentSet with another.

        Parameters
        ----------
        other
            The other SymbolicArgumentSet, which is compared with `self`.

        Returns
        -------
            True, if the signatures and the objects for all arguments
            correspond to each other.
        """

    def __hash__(self):
        pass
