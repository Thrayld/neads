from __future__ import annotations

from typing import Iterable, Sequence

from neads.activation_model.symbolic_objects.symbolic_object import SymbolicObject
from neads.activation_model.symbolic_objects.composite_object import CompositeObject


class ListObject(CompositeObject):
    """Subtype of CompositeObject for list of SymbolicObjects.

    The value of ListObject is a list whose entries are occupied by the
    values of corresponding sub-objects.
    """

    def __init__(self, *subobjects: SymbolicObject):
        """Create ListObject of given sub-objects.

        Parameters
        ----------
        subobjects
            SymbolicObjects which are sub-objects of created ListArgument.
            Their values will follow the order in which the objects were
            passed.
        """

        self._subobjects: Sequence[SymbolicObject] = subobjects

        # Check type of sub-objects
        for sub_obj in self._subobjects:
            if not isinstance(sub_obj, SymbolicObject):
                raise TypeError(
                    f'Given sub-object of ListObject is not instance of '
                    f'SymbolicObject: {sub_obj}'
                )

    def _perform_substitution(self, substitution_pairs) -> ListObject:
        """Actually perform substitution.

        Create ListObject whose entries are occupied by corresponding
        sub-objects after substitution.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            Copy of self with sub-objects after substitution.
        """

        sub_obj_after_substitution = [
            sub_obj._substitute_clean(substitution_pairs)
            for sub_obj in self._subobjects
        ]
        return ListObject(*sub_obj_after_substitution)

    def get_value(self):
        """Return a list of values of sub-objects of the ListObject.

        There must be no Symbol (i.e. free variable) in the ListObject.

        Returns
        -------
            List of values of sub-objects of the ListObject.

        Raises
        ------
        SymbolicObjectException
            If there are some Symbols left in the ListObject.
        """

        return [sub_obj.get_value() for sub_obj in self._subobjects]

    def __eq__(self, other: SymbolicObject) -> bool:
        """Perform comparison of `self` with the other SymbolicObject.

        Parameters
        ----------
        other
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            True, if the `other` is ListObject and sub-objects contained in
            `self` and `other` are pairwise value-equal (i.e. operator == is
            used). Otherwise False.
        """

        if isinstance(other, ListObject):
            if len(self._subobjects) == len(other._subobjects):
                # Check equality of corresponding sub-objects
                for sub_self, sub_other in zip(self._subobjects,
                                               other._subobjects):
                    if sub_self != sub_other:
                        return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def _get_subobjects(self) -> Iterable[SymbolicObject]:
        """Return an iterable of sub-objects which occur in the object.

        Returns
        -------
            An iterable of all sub-objects which occur in the ListObject.
        """

        return self._subobjects
