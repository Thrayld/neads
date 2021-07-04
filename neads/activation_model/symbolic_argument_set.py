from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Union, Callable, Sequence
import inspect

from .symbolic_objects import Value, ListObject, DictObject
from .symbolic_objects.symbolic_object import SymbolicObject

if TYPE_CHECKING:
    from .symbolic_objects import Symbol


class SymbolicArgumentSet:
    """Capture symbolic arguments of a function with given signature.

    Arguments for the function are SymbolicObjects which describes the shape
    of the actual arguments. The SymbolicArgumentSet allows substitution for
    the Symbols (any Symbol in the SymbolicObjects) to get the real
    arguments, with which the function may be called.

    The SymbolicArgumentSet is immutable, therefore any substitution produces
    a new instance of SymbolicArgumentSet, instead of modifying the original
    one.
    """

    def __init__(self, signature_bearer: Union[inspect.Signature, Callable],
                 /, *args, **kwargs):
        """Initialize SymbolicArgumentSet instance.

        The signature of a function is passed as the first argument followed
        by the actual arguments for the function.

        The arguments can be instances of SymbolicObject. The operations such
        as `substitute` and `get_actual_arguments` are performed on them.
        That is, values of those are used as the real arguments.

        Parameters
        ----------
        signature_bearer
            Signature of the function whose arguments are passed later.
        args
            Positional arguments for the function whose signature is passed.
        kwargs
            Keyword arguments for the function whose signature is passed.

        Raises
        ------
        TypeError
            If `signature_bearer` is not of type Signature nor Callable.
            If the arguments do not fit the signature.
        """

        self._signature = self._extract_signature(signature_bearer)
        bound = self._signature.bind(*args, **kwargs)
        bound.apply_defaults()

        conv_args, conv_kwargs = self._convert_to_symbolic_objects(bound)
        args = ListObject(*conv_args)
        kwargs = DictObject(conv_kwargs)

        self._bound_args_object = ListObject(args, kwargs)

    @property
    def signature(self):
        """Signature for the arguments."""
        raise NotImplementedError()

    @property
    def args(self) -> Sequence[SymbolicObject]:
        """SymbolicObjects of positional arguments."""
        raise NotImplementedError()

    @property
    def kwargs(self) -> dict[str, SymbolicObject]:
        """SymbolicObjects of keyword arguments."""
        raise NotImplementedError()

    @staticmethod
    def _extract_signature(
            signature_bearer: Union[inspect.Signature, Callable]
    ) -> inspect.Signature:
        """Extract and return signature from the `signature_bearer`.

        Parameters
        ----------
        signature_bearer
            Signature of a function.

        Returns
        -------
            Extracted signature.

        Raises
        ------
        TypeError
            If `signature_bearer` is not of type Signature nor Callable.
        """

        if isinstance(signature_bearer, inspect.Signature):
            return signature_bearer
        elif isinstance(signature_bearer, Callable):
            return inspect.signature(signature_bearer)
        else:
            raise TypeError(f'The first argument is not a Signature nor a '
                            f'Callable: {signature_bearer}')

    @staticmethod
    def _convert_to_symbolic_objects(bound: inspect.BoundArguments):
        """Convert given objects in BoundArguments to SymbolicArguments.

        If an argument is SymbolicObject, it is left as is. Otherwise,
        it is enclosed in Value object.

        Parameters
        ----------
        bound
            BoundArgument with objects (the arguments) which will be
            converted to SymbolicObject.

        Returns
        -------
            BoundArgument object with converted arguments.
        """

        converted_args = tuple(
            obj if isinstance(obj, SymbolicObject) else Value(obj)
            for obj in bound.args
        )
        converted_kwargs = {
            Value(key): (obj if isinstance(obj, SymbolicObject) else Value(obj))
            for key, obj in bound.kwargs.items()
        }

        return converted_args, converted_kwargs

    def get_symbols(self) -> Iterable[Symbol]:
        """Return an iterable of Symbols in arguments of type SymbolicObject.

        Returns
        -------
            An iterable of all Symbols which occur is at least one of the
            symbolic arguments.
        """

        return self._bound_args_object.get_symbols()

    def substitute(self, *args) -> SymbolicArgumentSet:
        """Substitute SymbolicObjects for Symbols in `self`.

        If a replacement occurs, new SymbolicArgumentSet is created from `self`,
        because SymbolicArgumentSet is immutable.

        Parameters
        ----------
        args
            One of the following:

            * Two arguments `symbol_from` and `object_to`.

            * Iterable with the pairs `symbol_from`, `object_to`.

            * Dict with `symbol_from` as keys and `object_to` as values.

        Returns
        -------
            SymbolicArgumentSet after substitution.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        ValueError
            If more than 2 arguments are passed, or one `symbol_from`
            occurs multiple times.
        """

        substituted = self._bound_args_object.substitute(*args)
        if substituted is self._bound_args_object:
            # No substitution occurred, it is save to return `self`
            return self
        else:
            # Substitution occurred, new SymbolicArgumentSet must be created
            sub_args, sub_kwargs = substituted
            # Convert sub_kwargs (DictObject) to something un-packable
            string_keys_kwargs = {
                key.get_value(): sub_kwargs[key]
                for key in sub_kwargs
            }
            return SymbolicArgumentSet(self._signature,
                                       *sub_args, **string_keys_kwargs)

    def get_actual_arguments(self, *args, copy=True, share=True
                             ) -> inspect.BoundArguments:
        """Return the actual arguments described by SymbolicArgumentSet.

        If there are Symbols (i.e. free variables) in the SymbolicArgumentSet,
        they must be replaced by some objects. Unlike in the `substitute`
        method, here the objects are not required to be instances of
        SymbolicObject.

        Parameters
        ----------
        args
            One of the following:

            * No arguments (`self` must be without Symbols).

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
            If the objects should be shared among all replacements for the
            particular Symbol. It depends on the `copy` argument, whether it
            will be the original object, or its copy.

            If `share` is False, each replacement of the Symbol have its
            own deepcopy of the original object.

            This argument is considered only if `copy` is True.

            Also note that in case of `copy` and `share` being True,
            one object won't be shared among occurrences of different Symbols
            (although the identical object were passed as a substitution for
            both Symbols). To arrange this behavior, one must perform
            a substitution of those Symbols first.

        Returns
        -------
            The actual bound arguments which the SymbolicArgumentSet describes.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        ValueError
            If more than 2 arguments are passed, or one `symbol_from`
            occurs multiple times.
        SymbolicArgumentSetException
            If there are some unsubstituted Symbols left in the
            SymbolicArgumentSet.
        """

        args, kwargs = self._bound_args_object.get_value(*args, copy=copy,
                                                         share=share)
        return self._signature.bind(*args, **kwargs)

    def __eq__(self, other: SymbolicArgumentSet) -> bool:
        """Compare the SymbolicArgumentSet with another.

        Parameters
        ----------
        other
            The other SymbolicArgumentSet, which is compared with `self`.

        Returns
        -------
            True, if the signatures and the objects for all arguments
            correspond to each other.
        """

        return self._bound_args_object == other._bound_args_object

    def __hash__(self):
        return hash(self._bound_args_object)


class SymbolicArgumentSetException(Exception):
    pass
