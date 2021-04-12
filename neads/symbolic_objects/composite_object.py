from typing import Iterable
import abc

from neads.symbolic_objects.symbolic_object import SymbolicObject
from neads.symbolic_objects.symbol import Symbol


class CompositeObject(SymbolicObject):
    """Subtype of SymbolicObject combining several sub-objects."""

    @abc.abstractmethod
    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
        """Do the substitution with iterable of pairs for substitution.

        If a replacement occurs, new CompositeObject is created from `self`,
        because SymbolicObject is immutable.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            CompositeObject after substitution.
        """

        pass

    def get_symbols(self) -> Iterable[Symbol]:
        """Return a list of Symbols which occur in the CompositeArgument.

        Returns
        -------
            A list of all symbols which occur in the CompositeArgument.
        """

        raise NotImplementedError()

        # subarguments = self._get_sub_arguments()
        # symbols_2d = [sub_arg.get_symbols() for sub_arg in subarguments]
        # symbols_iter = itertools.chain(*symbols_2d)
        # return set(symbols_iter)

    @abc.abstractmethod
    def get_value(self):
        """Return the object which the CompositeObject describes.

        There must be no Symbol (i.e. free variable) in the CompositeObject.

        Returns
        -------
            Object described by the CompositeObject.

        Raises
        ------
        SymbolicObjectException
            If there are some Symbols left in the CompositeObject.
        """

        pass

    @abc.abstractmethod
    def __eq__(self, other: SymbolicObject) -> bool:
        """Compare the CompositeObject with other SymbolicObject.

        Parameters
        ----------
        other
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            True, if the structure of both SymbolicObjects is the same and
            the Symbols are identical objects.
        """

        pass

    @abc.abstractmethod
    def _get_sub_arguments(self) -> Iterable[SymbolicObject]:
        """Return an iterable of sub-objects which occur in the object.

        Returns
        -------
            An iterable of all sub-objects which occur in the CompositeObject.
        """

        pass
