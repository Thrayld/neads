from typing import Iterable

from neads.symbolic_objects.symbolic_object import SymbolicObject
from neads.symbolic_objects.composite_object import CompositeObject


class DictObject(CompositeObject):
    """Subtype of CompositeObject for dict of SymbolicObjects.

    The value of DictObject is a dict whose key-value pairs are values of
    corresponding sub-objects.
    """

    def __init__(self, dict_of_objects: dict[SymbolicObject, SymbolicObject]):
        """Create DictObject of given sub-objects.

        Be ware of the fact, that object of type SymbolicObject may serve as
        a dictionary key, while its value may not (e.g. ListArgument and list).
        Do not use such objects as keys.

        Parameters
        ----------
        dict_of_objects
            Dictionary whose key-value pairs are pairs of SymbolicObjects.
        """

        pass

    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
        """Do the substitution with iterable of pairs for substitution.

        If a replacement occurs, new ListObject is created from `self`,
        because SymbolicObject is immutable.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            DictObject whose key-value pairs are sub-objects after
            substitution.
        """

        pass

    def get_value(self):
        """Return a dict of values of sub-objects of the DictObject.

        There must be no Symbol (i.e. free variable) in the DictObject.

        Returns
        -------
            Dict of values of sub-objects of the DictObject.

        Raises
        ------
        SymbolicObjectException
            If there are some Symbols left in the DictObject.
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
            True, if the `other` is DictObject and sub-objects contained in
            `self` and `other` are pairwise value-equal (i.e. operator == is
            used). Otherwise False.
        """

        pass

    def _get_sub_arguments(self) -> Iterable[SymbolicObject]:
        """Return an iterable of sub-objects which occur in the object.

        Returns
        -------
            An iterable of all sub-objects which occur in the DictObject.
        """

        pass
