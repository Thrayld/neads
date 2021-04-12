from __future__ import annotations

from typing import TYPE_CHECKING, Iterable
import abc

if TYPE_CHECKING:
    from neads.symbolic_objects.symbol import Symbol


class SymbolicObject(abc.ABC):
    """Capture shape of data structure using variables for true data.

    Support substitution for individual Symbols (i.e. variables). If the
    SymbolicObject is without Symbols, it can be transformed into the real
    object, which the SymbolicObject described.

    SymbolicObject is immutable, so any substitution
    """

    def substitute(self, *args) -> SymbolicObject:
        """Substitute SymbolicObjects for Symbols in `self`.

        If a replacement occurs, new SymbolicObject is created from `self`,
        because SymbolicObject is immutable.

        Parameters
        ----------
        args
            One of the following:

            * Two arguments `symbol_from` and object_to`.

            * Iterable with the pairs `symbol_from`, `object_to`.

            * Dict with `symbol_from` as keys and `object_to` as values.

        Returns
        -------
            SymbolicObject after substitution.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        """

        raise NotImplementedError()
        # Check types
        # Check that Symbol is present
        # If it is, substitute

        # # Check the types of both arguments
        # if not isinstance(symbol_now, Symbol):
        #     raise TypeError(
        #         f"Argument 'symbol_now' has wrong type: {type(symbol_now)}"
        #     )
        # elif not isinstance(symbol_then, Symbol):
        #     raise TypeError(
        #         f"Argument 'symbol_then' has wrong type: {type(symbol_then)}"
        #     )
        #
        # return self._substitute_symbol_clean(symbol_now, symbol_then)

    @abc.abstractmethod
    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
        """Do the substitution with iterable of pairs for substitution.

        If a replacement occurs, new SymbolicObject is created from `self`,
        because SymbolicObject is immutable.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            SymbolicObject after substitution.
        """

        pass

    @abc.abstractmethod
    def get_symbols(self) -> Iterable[Symbol]:
        """Return a list of Symbols which occur in the SymbolicObject.

        Returns
        -------
            A list of all symbols which occur in the SymbolicObject.
        """

        pass

    @abc.abstractmethod
    def get_value(self):
        """Return the object which the SymbolicObject describes.

        There must be no Symbol (i.e. free variable) in the SymbolicObject.

        Returns
        -------
            Object described by the SymbolicObject.

        Raises
        ------
        SymbolicObjectException
            If there are some Symbols left in the SymbolicObject.
        """

        # IDEA: return without copy
        pass

    @abc.abstractmethod
    def __eq__(self, other: SymbolicObject) -> bool:
        """Compare the SymbolicObject with the other SymbolicObject.

        The algorithm first compares head of the SymbolicObject and (if they
        agree) recursively compares structures of corresponding sub-objects.

        The natural comparison by value applies. Only the Symbols
        are implement reference comparison, i.e. they must be the same Python
        objects to be compared with True result.

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
