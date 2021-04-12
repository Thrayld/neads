from __future__ import annotations

from typing import Iterable

from symbolic_object import SymbolicObject


class Symbol(SymbolicObject):
    """Symbol, i.e. free variable in a SymbolicObject."""

    def __init__(self):
        pass

    def _substitute_clean(self, substitution_pairs):
        """Apply substitution on Symbol.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            `Self`, if the Symbol in not included in `substitution_pairs` as
            one of the `symbol_from`. Otherwise, the corresponding `object_to`.
        """
        pass

    def get_symbols(self) -> Iterable[Symbol]:
        """Return (`self`,) as the only symbol.

        Returns
        -------
            Return (`self`,) as the only symbol.
        """
        pass

    def get_value(self):
        """Raise exception as Symbol cannot be transferred to value.

        Raises
        ------
        SymbolicObjectException
            Symbol cannot be transferred to value.
        """
        pass

    def __eq__(self, other: SymbolicObject) -> bool:
        """Reference-wise compares `self` with the `other` SymbolicObject.

        Parameters
        ----------
        other
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            Result of the expression: `self` is `other`.
        """

        pass
