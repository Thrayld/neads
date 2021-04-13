from __future__ import annotations

from typing import Iterable
import abc
import itertools

from neads.symbolic_objects.symbolic_object import SymbolicObject, Symbol


class CompositeObject(SymbolicObject):
    """Subtype of SymbolicObject combining several sub-objects."""

    def _substitute_clean(self, substitution_pairs) -> CompositeObject:
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

        if self._is_affected_by_substitution(substitution_pairs):
            return self._perform_substitution(substitution_pairs)
        else:
            return self

    def _is_affected_by_substitution(self, substitution_pairs) -> bool:
        """Return whether the object is affected by substitution.

        Whether the object is affected by substitution, i.e. one of
        `symbol_from` symbols in `substitution_pairs` is a Symbol in the
        object.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            Whether the object is affected by substitution.
        """

        self_symbols = set(self.get_symbols())
        symbol_to_substitute = set(symbol for symbol, object
                                   in substitution_pairs)
        common_symbols = self_symbols.intersection(symbol_to_substitute)
        return len(common_symbols) > 0

    @abc.abstractmethod
    def _perform_substitution(self, substitution_pairs) -> CompositeObject:
        """Actually perform substitution.

        Create copy of self with sub-objects after substitution (i.e.
        potentially new instances).

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            Copy of self with sub-objects after substitution.
        """

        pass

    def get_symbols(self) -> Iterable[Symbol]:
        """Return a list of Symbols which occur in the CompositeArgument.

        Returns
        -------
            A list of all symbols which occur in the CompositeArgument.
        """

        subarguments = self._get_subobjects()
        symbols_2d = [sub_arg.get_symbols() for sub_arg in subarguments]
        symbols_iter = itertools.chain(*symbols_2d)
        return set(symbols_iter)

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
    def _get_subobjects(self) -> Iterable[SymbolicObject]:
        """Return an iterable of sub-objects which occur in the object.

        Returns
        -------
            An iterable of all sub-objects which occur in the CompositeObject.
        """

        pass
