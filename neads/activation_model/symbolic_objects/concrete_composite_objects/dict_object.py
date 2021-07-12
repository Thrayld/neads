from __future__ import annotations

from typing import Iterable
import collections.abc
import itertools

from frozendict import frozendict

from neads.activation_model.symbolic_objects.symbolic_object import \
    SymbolicObject
from neads.activation_model.symbolic_objects.composite_object import \
    CompositeObject


class DictObject(collections.abc.Mapping, CompositeObject):
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

        self._dict_subobjects = frozendict(dict_)

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

        s_p = substitution_pairs  # Assign to a variable with shorter name
        dict_after_subs = {
            key.substitute(s_p): val.substitute(s_p)
            for key, val in self._dict_subobjects.items()
        }
        return DictObject(dict_after_subs)

    def _get_value_clean(self, substitution_pairs, share):
        """Return a dict of values of sub-objects of the DictObject.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.
        share
            Whether the given object for a Symbol should be shared
            among all replacements for the particular Symbol.

        Returns
        -------
            Dict of values of sub-objects of the DictObject.

        Raises
        ------
        SymbolicObjectException
            If there are still some Symbols left in the DictObject.
        """

        s_p = substitution_pairs  # Assign to a variable with shorter name
        dict_value = {
            key._get_value_clean(s_p, share): val._get_value_clean(s_p, share)
            for key, val in self._dict_subobjects.items()
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
            return self._dict_subobjects == other._dict_subobjects
        else:
            return False

    def _get_subobjects(self) -> Iterable[SymbolicObject]:
        """Return an iterable of sub-objects which occur in the object.

        Returns
        -------
            An iterable of all sub-objects which occur in the DictObject.
        """

        items_pairs = self._dict_subobjects.items()
        return (item for item in itertools.chain(*items_pairs))

    def __hash__(self):
        return hash(self._dict_subobjects)

    def __iter__(self):
        return iter(self._dict_subobjects)

    def __len__(self) -> int:
        return len(self._dict_subobjects)

    def __getitem__(self, key):
        return self._dict_subobjects[key]

    def __str__(self):
        content = ', '.join(map(lambda kv: f'{kv[0]}: {kv[1]}',
                                self._dict_subobjects.items()))
        return f'DictObject({{{ content }}})'
