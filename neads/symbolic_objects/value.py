from typing import Iterable

from neads.symbolic_objects.symbolic_object import SymbolicObject, Symbol


class Value(SymbolicObject):
    """Concrete value in a SymbolicObject."""

    def __init__(self, value):
        """Initialize Value with its content.

        The given object is copied in order to be able to maintain
        immutability of SymbolicObjects.

        Parameters
        ----------
        value
            Object which the Value held.
        """

        self._value = value

    def _substitute_clean(self, substitution_pairs):
        """Apply substitution on Value.

        No substitution can actually occur in Value, so always the original
        Value is returned.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            `Self`, as no substitution can occur.
        """
        pass

    def get_symbols(self) -> Iterable[Symbol]:
        """Return empty tuple for Symbols in Value.

        Returns
        -------
            Empty tuple, as Value has no Symbols.
        """
        pass

    def get_value(self):
        """Return the actual value, which the Value contains.

        The value is copied in order to maintain immutability of Value as
        SymbolicObject in general. Thus, changes in the returned object do
        not affect the Value or any SymbolicObject in which is contained.

        Returns
        -------
            The actual value, which the Value contains.
        """
        pass

    def __eq__(self, other: SymbolicObject) -> bool:
        """Perform comparison of `self` with the other SymbolicObject.

        Parameters
        ----------
        other
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            True, if the `other` is Value and object contained in `self` and
            `other` are value-equal (i.e. operator == is used). Otherwise False.
        """

        pass