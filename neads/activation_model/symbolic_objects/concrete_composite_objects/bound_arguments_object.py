from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Iterable, Tuple

from frozendict import frozendict

from neads.activation_model.symbolic_objects.symbolic_object import \
    SymbolicObject
from neads.activation_model.symbolic_objects.composite_object import \
    CompositeObject

if TYPE_CHECKING:
    import inspect


class BoundArgumentObject(CompositeObject):
    """Subtype of CompositeObject for BoundArguments of type SymbolicObject.

    The value of BoundArguments is a `inspect.BoundArguments` such that the
    arguments are the values the sub-objects.
    """

    def __init__(self, signature, /,
                 *args: SymbolicObject, **kwargs: SymbolicObject):
        """Create BoundArgumentsObject of given sub-objects.

        The signature of a function is passed as the first argument followed
        by the actual arguments for the function as SymbolicObjects.

        Parameters
        ----------
        signature_bearer
            Signature of the function whose arguments are passed later.
        args
            Positional arguments for the function whose signature is passed.
        kwargs
            Keyword arguments for the function whose signature is passed.
        """

        raise NotImplementedError()

        self._signature = signature
        self._args: Tuple[SymbolicObject] = args
        self._kwargs = frozendict(kwargs)

        # Check type of sub-objects
        for args in itertools.chain(self._args, self._kwargs):
            if not isinstance(args, SymbolicObject):
                raise TypeError(
                    f'Given value of argument in BoundArgumentObject is not '
                    f'instance of SymbolicObject: {args}'
                )

    def _perform_substitution(self, substitution_pairs) -> BoundArgumentObject:
        """Actually perform substitution.

        Create BoundArgumentsObject whose arguments are the corresponding
        sub-objects after substitution.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            Copy of self with arguments being the sub-objects after
            substitution.
        """

        raise NotImplementedError()

        sub_obj_after_substitution = [
            sub_obj._substitute_clean(substitution_pairs)
            for sub_obj in self._subobjects
        ]
        return BoundArgumentObject(*sub_obj_after_substitution)

    def _get_value_clean(self, substitution_pairs, share) \
            -> inspect.BoundArguments:
        """Return BoundArguments of the signature with values of sub-objects.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.
        share
            Whether the given object for a Symbol should be shared
            among all replacements for the particular Symbol.

        Returns
        -------
            BoundArguments of the signature with values of the sub-objects.

        Raises
        ------
        SymbolicObjectException
            If there are still some Symbols left in the BoundArgumentsObject.
        """

        raise NotImplementedError()

        return [sub_obj._get_value_clean(substitution_pairs, share)
                for sub_obj in self._subobjects]

    def __eq__(self, other: SymbolicObject) -> bool:
        """Perform comparison of `self` with the other SymbolicObject.

        Parameters
        ----------
        other
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            True, if the `other` is BoundArgumentsObject and the arguments
            correspond to each other.
        """

        raise NotImplementedError()

        if isinstance(other, ListObject):
            return self._subobjects == other._subobjects
        else:
            return False

    def _get_subobjects(self) -> Iterable[SymbolicObject]:
        """Return an iterable of sub-objects which occur in the object.

        Returns
        -------
            An iterable of all sub-objects which occur in the
            BoundedArgumentsObject.
        """

        raise NotImplementedError()

        return self._subobjects

    def __hash__(self):

        raise NotImplementedError()

        return hash(self._subobjects)
