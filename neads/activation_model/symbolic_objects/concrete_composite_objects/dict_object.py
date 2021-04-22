from __future__ import annotations

from typing import Iterable
import itertools

from neads.activation_model.symbolic_objects.symbolic_object import SymbolicObject
from neads.activation_model.symbolic_objects.composite_object import CompositeObject


class DictObject(CompositeObject):
    """Subtype of CompositeObject for dict of SymbolicObjects.

    The value of DictObject is a dict whose key-value pairs are values of
    corresponding sub-objects.

    Be ware of the fact that object of type SymbolicObject may serve as
    a dictionary key, while its value may not (e.g. ListArgument and list).
    Do not use such objects as keys. DictObject checks this condition only in
    get_value method, which is rather late.
    """

    def __init__(self, dict_: dict[SymbolicObject, SymbolicObject]):
        """Create DictObject of given sub-objects.

        Parameters
        ----------
        dict_
            Dictionary whose key-value pairs are pairs of SymbolicObjects.
        """

        # Check types of argument
        for key, val in dict_.items():
            for sub_obj in (key, val):
                if not isinstance(sub_obj, SymbolicObject):
                    raise TypeError(
                        f'Given sub-object of ListObject is not instance of '
                        f'SymbolicObject: {sub_obj}'
                    )

        self._key_val_subobjects = dict_.items()

    def _perform_substitution(self, substitution_pairs) -> DictObject:
        """Actually perform substitution.

        Create DictObject whose key-value pair are the corresponding
        sub-objects after substitution.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            Copy of self with sub-objects after substitution.
        """

        items_after_subs = (
            (
                key.substitute(substitution_pairs),
                val.substitute(substitution_pairs)
            )
            for key, val in self._key_val_subobjects
        )
        dict_ = dict(items_after_subs)
        return DictObject(dict_)

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

        dict_value = {
            key.get_value(): val.get_value()
            for key, val in self._key_val_subobjects
        }
        return dict_value

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

        if isinstance(other, DictObject):
            if len(self._key_val_subobjects) == len(other._key_val_subobjects):
                # Check equality of corresponding sub-objects
                for sub_self, sub_other in zip(self._key_val_subobjects,
                                               other._key_val_subobjects):
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
            An iterable of all sub-objects which occur in the DictObject.
        """

        return (item for item in itertools.chain(*self._key_val_subobjects))
