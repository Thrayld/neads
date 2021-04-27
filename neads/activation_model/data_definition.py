from __future__ import annotations

from typing import Optional, Dict, Hashable
import functools

from .symbolic_objects import Value
from .symbolic_objects import Symbol
from .symbolic_argument_set import SymbolicArgumentSet


class DataDefinition:
    """Capture history of the data produced by a function with given arguments.

    The DataDefinition allows you instantly compare results of two calling
    chains (if they are already captured in DataDefinition object) even
    before the results are actually computed, provided that the functions in
    the chains are pure (i.e. their result can be determined solely by their
    arguments).

    The instances are also hashable and works well with pickle module.

    Notes
    -----
        As a 'pure' function we consider those functions which comply with the
        first property in the definition of a pure function on wikipedia.
        That is, when called with the same arguments (here compared by ==)
        the function produces the same results.

        Also, note that the second property might be very important when
        utilizing DataDefinitions. Specially for the purpose of memoization,
        when the function is not actually called and an already computed
        result is returned instead. This might be problematic when used with
        non-pure function, if the surrounding code expects some side effects
        to occur.

        https://en.wikipedia.org/wiki/Pure_function
        https://en.wikipedia.org/wiki/Memoization
    """

    class _MyGuard:
        """Serve as signal to outside world that __init__ in should not be used.

        The idea is that the type checker can detect (in some cases) invalid
        access to DataDefinition.__init__ from outside.
        """

    _guard = _MyGuard()
    _instances = {}

    @staticmethod
    def get_instance(
        function_id: Hashable,
        arguments: SymbolicArgumentSet,
        symbols_definitions: Optional[Dict[Symbol, DataDefinition]] = None
    ) -> DataDefinition:
        """Return a DataDefinition for object described by the arguments.

        Either a new DataDefinition instance is created or already existing
        instances is reused. It depends, whether the instance for the
        same object that describe the given arguments, has been already
        created.

        It is possible to pass SymbolicArgumentSet with Symbols. However,
        in that case, mapping from the Symbols to corresponding DataDefinitions
        must be provided.

        Parameters
        ----------
        function_id
            Unique identifier the function, i.e. two functions with the same
            `function_id` are considered to be equal. It must be hashable.
        arguments
            Symbolic description of arguments of the function whose id is
            given. It must be hashable.
        symbols_definitions
            Definitions of Symbols in the SymbolicArgumentSet. That is,
            DataDefinition of the objects which are supposed to be substituted
            for the Symbols.

        Returns
        -------
            Either new or re-used DataDefinition instance

        Raises
        ------
        TypeError
            If there is a type mismatch against the specification or
            `function_id` or `arguments` is not hashable.
        ValueError
            If an instance of DataDefinition is not provided for all Symbols.
        """

        symbols_definitions = symbols_definitions \
            if symbols_definitions is not None \
            else {}

        # Type checking
        if not isinstance(arguments, SymbolicArgumentSet):
            raise TypeError(f"'Arguments' is not an instance of "
                            f"SymbolicArgumentSet: {arguments}")
        for sym, ddf in symbols_definitions.items():
            if not isinstance(sym, Symbol):
                raise TypeError(f"Key in 'symbols_definitions' dict is not an "
                                f"instance of Symbol: {sym}")
            if not isinstance(arguments, SymbolicArgumentSet):
                raise TypeError(f"Value in 'symbols_definitions' dict is not "
                                f"an instance of Symbol: {ddf}")

        norm_arguments = DataDefinition._get_normalized_argument_set(
            arguments, symbols_definitions)

        # Create look-up key for instance
        key = (function_id, norm_arguments)
        try:
            # If already same instances already exists
            if None is (inst := DataDefinition._instances.get(key)):
                # New instance is initialized and stored in `_instances` dict
                new_inst = DataDefinition(DataDefinition._guard,
                                          function_id,
                                          norm_arguments)
                DataDefinition._instances[key] = new_inst
                return new_inst
            else:
                # Instance was found - we can return it
                return inst
        except TypeError as e:
            # The hash-ability is preserved while normalizing arguments
            # If there is a problem, it was present when the argument was passed
            raise TypeError(
                f"Either 'function_id' or the 'arguments' are not hashable: "
                f"{function_id}, {arguments}"
            ) from e

    @staticmethod
    def _get_normalized_argument_set(arguments, symbols_definitions):
        """Return normalized argument set suitable for comparing.

        Parameters
        ----------
        arguments
            Symbolic description of arguments of the function whose id is
            given. It must be hashable.
        symbols_definitions
            Definitions of Symbols in the SymbolicArgumentSet. That is,
            DataDefinition of the objects which are supposed to be substituted
            for the Symbols.

        Returns
        -------
            Normalized argument set suitable for comparing. That is,
            the DataDefinitions (inside Value) are substituted for
            corresponding Symbols.

        Raises
        ------
        ValueError
            If an instance of DataDefinition is not provided for all Symbols.
        """

        # If there are instructions for substitution
        if symbols_definitions:
            substitution_pairs = {
                sym: Value(ddf)
                for sym, ddf in symbols_definitions.items()
            }
            normalized_args = arguments.substitute(substitution_pairs)
        else:
            normalized_args = arguments

        if len(remaining := normalized_args.get_symbols()) == 0:
            return normalized_args
        else:
            raise ValueError(f'For at least one symbol, no DataDefinition '
                             f'instance was provided: {remaining}')

    def __init__(self, guard: _MyGuard, function_id, arguments):
        """Initialize a DataDefinition instance.

        The method is NOT MEANT to be used from outside the class. Use
        `get_instance` method to obtain instances of DataDefinition instead.
        """

        if guard is not DataDefinition._guard:
            raise DataDefinitionException(
                "DataDefinition.__init__ method is not meant to be used for "
                "outside the class. Use 'get_instance' method to obtain "
                "instances of DataDefinition instead."
            )

        self._function_id = function_id
        self._arguments = arguments

    def __reduce_ex__(self, protocol):
        """To support pickling."""

        return DataDefinition.get_instance, (self._function_id, self._arguments)


class DataDefinitionException(Exception):
    pass
