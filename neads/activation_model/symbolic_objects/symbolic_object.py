from __future__ import annotations

from typing import Iterable, Sequence
import abc
from collections import Counter

from neads.activation_model.symbolic_objects.symbolic_object_exception \
    import SymbolicObjectException


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

            * Two arguments `symbol_from` and `object_to`.

            * Iterable with the pairs `symbol_from`, `object_to`.

            * Dict with `symbol_from` as keys and `object_to` as values.

        Returns
        -------
            `Self`, if none substitution occurs. Otherwise, SymbolicObject
            after substitution.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        ValueError
            If 0 or more than 2 arguments are passed, or one `symbol_from`
            occurs multiple times.

        See Also
        --------
            `get_value` for discussion on differences between
            `substitute` and `get_value`
        """

        # If pair `symbol_from`, `object_to` is passed
        if len(args) == 2:
            substitution_pairs = (args,)
        # If one arg is passed, its either dict or pairs directly
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, dict):
                substitution_pairs = arg.items()
            else:
                substitution_pairs = arg
        else:
            raise ValueError(f'Invalid number of arguments passed: {len(args)}')

        self._check_substitution_pairs(substitution_pairs)
        return self._substitute_clean(substitution_pairs)

    @staticmethod
    def _check_substitution_pairs(substitution_pairs):
        """Check that given object is valid iterable of substitution pairs.

        That is, the object is iterable of pairs (sequence of length 2).
        The first element is a pair occur only once among first elements
        (i.e. given Symbol has uniquely determined `object_to`).
        Then, type of the first element in a pair is Symbol, type of the second
        element is SymbolicObject.

        Parameters
        ----------
        substitution_pairs
            Candidate for substitution_pairs object.

        Raises
        ------
        ValueError
            If one Symbol occurs multiple times as `symbol_from`, i.e. as
            the first element of pair.
        TypeError
            If there is any other problem with substitution pairs object,
            as listed above.
        """

        if isinstance(substitution_pairs, Iterable):
            # Check each item individually
            for item in substitution_pairs:
                # If item is a pair
                if isinstance(item, Sequence) and len(item) == 2:
                    first, second = item
                    # Check types of elements of the pair
                    if not isinstance(first, Symbol):
                        raise TypeError(
                            f'First element in pair has wrong type: '
                            f'{first}, {type(first)}'
                        )
                    if not isinstance(second, SymbolicObject):
                        raise TypeError(
                            f'Second element in pair has wrong type: '
                            f'{second}, {type(second)}'
                        )
                else:
                    raise TypeError(
                        f'Item of substitution pairs iterable is not '
                        f'a pair: {item}'
                    )
            # Check that each `symbol_from` appears at most once
            cnt = Counter(symbol_from for symbol_from, object_to
                          in substitution_pairs)
            max_symbol, max_count = cnt.most_common(1)[0]
            if max_count > 1:
                raise ValueError(
                    f"Symbol appears multiple times as 'symbol_from': "
                    f"{max_symbol}"
                )
        else:
            raise TypeError(
                f'Substitution pairs argument is not iterable: '
                f'{substitution_pairs}'
            )

    @abc.abstractmethod
    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
        """Do the substitution with iterable of pairs for substitution.

        If a replacement occurs, new SymbolicObject is created from `self`,
        because SymbolicObject is immutable.

        The `substitution_pairs` are check to be a clean arguments.

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
        """Return an iterable of Symbols which occur in the SymbolicObject.

        Returns
        -------
            An iterable of all symbols which occur in the SymbolicObject.
        """

        # IDEA: What about establishing an order and returning a sequence?
        pass

    def get_value(self, *args, copy=True, share=True):
        """Return the object which the SymbolicObject describes.

        If there are Symbols (i.e. free variables) in the SymbolicObject,
        they must be replaced by some objects. The objects are handled as
        they are, unlike in `substitute` method, where only SymbolicObjects
        are allowed (and a real value extracted is from them).

        Parameters
        ----------
        args
            One of the following:

            * No argument, if there is no Symbol left in the SymbolicObject.

            * Two arguments `symbol_from` and `object_to`.

            * Iterable with the pairs `symbol_from`, `object_to`.

            * Dict with `symbol_from` as keys and `object_to` as values.
        copy
            Whether a deep copy of given objects should appear in the
            resulting arguments.

            It is safer to create the copy to prevent intertwining between
            the original objects and the objects in the arguments. The
            modification of non-copied objects may result in unexpected
            behavior.
        share
            Whether one deepcopy of the original object should be shared
            among all replacements for the particular Symbol.
            If not, each replacement of the Symbol have its own deepcopy
            of the original object.

            This argument is considered only if `copy` is True.

            Also note that in case of `copy` and `share` being True,
            one object won't be shared among occurrences of different Symbols
            (although the identical object were passed as a substitution for
            both Symbols). To arrange this behavior, one must perform
            a substitution of those Symbols first.

        Returns
        -------
            Object described by the SymbolicObject.

        Raises
        ------
        SymbolicObjectException
            If there are still some Symbols left in the SymbolicObject.

        Notes
        -----
            There are a few differences between `get_value` and `substitute`
            methods.

            Returned object:
            * `get_value` returns an object
            * `substitute` returns SymbolicObject

            Replacement for Symbols:
            * `get_value` accepts any object
            * `substitute` requires SymbolicObject

            Remaining Symbols:
            * When calling `get_value`, all Symbols must be substituted
            * When calling `substitute`, some Symbols may remain

            Copying input objects:
            * `get_value` copies them once by default (per each replacement)
            * When using `substitute` (and `get_value` later), objects must
            be copied twice (to ensure immutability of SymbolicObject)
        """

        # TODO: add substitution with / without copy
        # IDEA: return without copy
        pass

    @abc.abstractmethod
    def _get_value_clean(self, substitution_pairs, copy=True):
        """Do return the object which the SymbolicObject describes.

        The `substitution_pairs` are check to be a clean arguments.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.
        copy
            Whether a deep copy of given objects should appear in the
            resulting arguments.

        Returns
        -------
            SymbolicObject after substitution.
        """

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
            The other SymbolicObject, which is compared with `self`.

        Returns
        -------
            True, if the structure of both SymbolicObjects is the same and
            the Symbols are identical objects.
        """

        pass

    @abc.abstractmethod
    def __hash__(self):
        pass


class Symbol(SymbolicObject):
    """Symbol, i.e. free variable in a SymbolicObject."""

    def __init__(self):
        pass

    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
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

        for symbol_from, object_to in substitution_pairs:
            if symbol_from == self:
                return object_to
        else:
            # If on `self` is no substitution request
            return self

    def get_symbols(self) -> Iterable[Symbol]:
        """Return (`self`,) as the only symbol.

        Returns
        -------
            Return (`self`,) as the only symbol.
        """

        return self,

    def get_value(self):
        """Raise exception as Symbol cannot be transferred to value.

        Raises
        ------
        SymbolicObjectException
            Symbol cannot be transferred to value.
        """

        # TODO: add substitution with / without copy
        raise SymbolicObjectException('Symbol cannot be transferred to value.')

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

        return self is other

    def __hash__(self):
        return id(self)
