from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Union, Callable
import inspect
import itertools

from .symbolic_objects import Value
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
        by the actual arguments for the function. Some of them might be
        instances of SymbolicObject.

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

        self._bound_args = self._convert_to_symbolic_objects(bound)

        # Serves as a cache
        # It does not hurt to create it eagerly, it is used everywhere anyway
        # self._arguments_iterable: Tuple[SymbolicObject] = tuple(
        #     *self._bound_args.args,
        #     *self._bound_args.kwargs.items()
        # )

    def _extract_signature(
            self,
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

    def _convert_to_symbolic_objects(self, bound: inspect.BoundArguments) \
            -> inspect.BoundArguments:
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
            key: (obj if isinstance(obj, SymbolicObject) else Value(obj))
            for key, obj in bound.kwargs.items()
        }

        return self._signature.bind(*converted_args, **converted_kwargs)

    def get_symbols(self) -> Iterable[Symbol]:
        """Return an iterable of Symbols occurring in argument's SymbolicObject.

        Returns
        -------
            An iterable of all Symbols which occur is at least of the symbolic
            arguments.
        """

        args_symbols = [arg.get_symbols()
                        for arg in self._bound_args.args]
        kwargs_symbols = [arg.get_symbols()
                          for arg in self._bound_args.kwargs.values()]
        return set(itertools.chain(*args_symbols, *kwargs_symbols))

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
            If 0 or more than 2 arguments are passed, or one `symbol_from`
            occurs multiple times.
        """

        def _substitution_occurred():
            """Whether at least one of the arguments has changed."""
            for arg, sub_arg in zip(self._bound_args.args, subs_args):
                if arg is not sub_arg:
                    return True
            for arg, sub_arg in zip(self._bound_args.kwargs, subs_kwargs):
                if arg is not sub_arg:
                    return True
            return False

        substitution_instruction = args

        subs_args = [arg.substitute(*substitution_instruction)
                     for arg in self._bound_args.args]
        subs_kwargs = {key: arg.substitute(*substitution_instruction)
                       for key, arg in self._bound_args.kwargs.items()}

        if _substitution_occurred():
            return SymbolicArgumentSet(self._signature,
                                       *subs_args, **subs_kwargs)
        else:
            return self

    def get_actual_arguments(self, *args, copy=True) -> inspect.BoundArguments:
        """Return the actual arguments described by SymbolicArgumentSet.

        If there are Symbols (i.e. free variables) in the SymbolicObject,
        they must be replaced by some objects. Unlike in the `substitute`
        method, here the objects are not required to be instances of
        SymbolicObject.

        Parameters
        ----------
        args
            One of the following:

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

        Returns
        -------
            The actual bound arguments which the SymbolicArgumentSet describes.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        ValueError
            If 0 or more than 2 arguments are passed, or one `symbol_from`
            occurs multiple times.
        SymbolicObjectException
            If there are some unsubstituted Symbols left in the
            SymbolicArgumentSet.
        """

        substitution_instruction = args

        subs_args = [arg.get_value(*substitution_instruction, copy)
                     for arg in self._bound_args.args]
        subs_kwargs = {key: arg.get_value(*substitution_instruction, copy)
                       for key, arg in self._bound_args.kwargs.items()}

        return self._signature.bind(*subs_args, **subs_kwargs)

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

        return self._bound_args == other._bound_args

    def __hash__(self):
        return hash(self._bound_args)
