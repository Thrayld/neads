from __future__ import annotations

from typing import Iterable, Union, List
import abc
import itertools


class SymbolicArgumentException(Exception):
    pass


class SymbolicArgument(abc.ABC):
    """Capture syntactic shape of an argument.

    Support substitution for individual Symbols (i.e. variables). If the
    SymbolicArgument is without Symbols, it can be transformed into the real
    argument.
    """

    def substitute_symbol(self, symbol_now: Symbol, symbol_then: Symbol):
        """Substitute a Symbol for one of current Symbols.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `symbol_then` Symbol in the
            SymbolicArgument.
        symbol_then
            Symbol which replaces the `symbol_now` Symbol in the
            SymbolicArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. `symbol_now` was present in
            the SymbolicArgument. False otherwise.

        Raises
        ------
        TypeError
            If type of either `symbol_now` or `symbol_then` is not Symbol.
        """

        # Check the types of both arguments
        if not isinstance(symbol_now, Symbol):
            raise TypeError(
                f"Argument 'symbol_now' has wrong type: {type(symbol_now)}"
            )
        elif not isinstance(symbol_then, Symbol):
            raise TypeError(
                f"Argument 'symbol_then' has wrong type: {type(symbol_then)}"
            )

        return self._substitute_symbol_clean(symbol_now, symbol_then)

    @abc.abstractmethod
    def _substitute_symbol_clean(self, symbol_now: Symbol, symbol_then: Symbol):
        """Do the symbol substitution with clean arguments.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `symbol_then` Symbol in the
            SymbolicArgument.
        symbol_then
            Symbol which replaces the `symbol_now` Symbol in the
            SymbolicArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. `symbol_now` was present in
            the SymbolicArgument. False otherwise.
        """
        pass

    def substitute_value(self, symbol_now: Symbol, value_then: Value):
        """Substitute a Value for one of current Symbols.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `value_then` Value in the
            SymbolicArgument.
        value_then
            Value which replaces the `symbol_now` Symbol in the
            SymbolicArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. `symbol_now` was present in
            the SymbolicArgument. False otherwise.

        Raises
        ------
        TypeError
            If type `symbol_now` is not Symbol or type of `value_then` is not
            Value.
        """

        # Check the types of both arguments
        if not isinstance(symbol_now, Symbol):
            raise TypeError(
                f"Argument 'symbol_now' has wrong type: {type(symbol_now)}"
            )
        elif not isinstance(value_then, Value):
            raise TypeError(
                f"Argument 'value_then' has wrong type: {type(value_then)}"
            )

        return self._substitute_value_clean(symbol_now, value_then)

    @abc.abstractmethod
    def _substitute_value_clean(self, symbol_now: Symbol, value_then: Value):
        """Do the value substitution with clean arguments.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `value_then` Value in the
            SymbolicArgument.
        value_then
            Value which replaces the `symbol_now` Symbol in the
            SymbolicArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. `symbol_now` was present in
            the SymbolicArgument. False otherwise.
        """

        pass

    @abc.abstractmethod
    def get_symbols(self) -> Iterable[Symbol]:
        """Return a list of Symbols which occur in the SymbolicArgument.

        Returns
        -------
            A list of all symbols which occur in the SymbolicArgument.
        """

        pass

    @abc.abstractmethod
    def get_actual_argument_value(self):
        """Return the value which the SymbolicArgument describes.

        There must be no Symbol (i.e. free variable) in the SymbolicArgument.

        Returns
        -------
            Real value described by the SymbolicArgument.

        Raises
        ------
        SymbolicArgumentException
            If there are some Symbols left in the SymbolicArgument.
        """

        pass


class SimpleArgument(SymbolicArgument):
    """Subtype of SymbolicArgument containing a single Symbol or Value.

    Elementary subtype of SymbolicArgument, which only contains a single
    instance of Symbol or a single instance of Value. It effectively hides
    operations with these basic building blocks.
    """

    def __init__(self, content: Union[Symbol, Value]):
        """Create SimpleArgument with the given symbol.

        Parameters
        ----------
        content
            Symbol or Value, which is contained in the created SymbolicArgument.
        """

        if not isinstance(content, Symbol) and not isinstance(content, Value):
            raise TypeError(
                f'Argument of SimpleArgument is neither Symbol nor Value: '
                f'{type(content)}'
            )

        self._content = content

    def _substitute_symbol_clean(self, symbol_now: Symbol, symbol_then: Symbol):
        """Do the symbol substitution with clean arguments.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `symbol_then` Symbol in the
            SimpleArgument.
        symbol_then
            Symbol which replaces the `symbol_now` Symbol in the
            SimpleArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. symbol_now was present in
            the SimpleArgument. False otherwise.
        """

        if self._has_symbol():
            if self._content == symbol_now:
                # Substitution is possible
                self._content = symbol_then
                return True
            else:
                # Symbol to be taken out is different from held symbol
                return False
        else:
            # SimpleArgument holds a Value, which cannot be substituted
            return False

    def _substitute_value_clean(self, symbol_now: Symbol, value_then: Value):
        """Do the value substitution with clean arguments.

        The replacement occur only if the `symbol_now` correspond to the
        Symbol held by the SimpleArgument (in case it even holds a Symbol).

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `value_then` Value in the
            SimpleArgument.
        value_then
            Value which replaces the `symbol_now` Symbol in the
            SimpleArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. `symbol_now` was present in
            the SimpleArgument. False otherwise.

        Raises
        ------
        TypeError
            If either of the arguments has a wrong type.
        """

        if self._has_symbol():
            if self._content == symbol_now:
                # Substitution is possible
                self._content = value_then
                return True
            else:
                # Symbol to be taken out is different from held symbol
                return False
        else:
            # SimpleArgument holds a Value, which cannot be substituted
            return False

    def get_symbols(self) -> Iterable[Symbol]:
        """Return a list of Symbols which occur in the SymbolicArgument.

        Returns
        -------
            A list of all symbols which occur in the SymbolicArgument.
        """

        if self._has_symbol():
            # Symbol is the actual type of self._content
            # Thus the type of return value correspond to type hint

            # noinspection PyTypeChecker
            return [self._content]
        else:
            return []

    def get_actual_argument_value(self):
        """Return the value which the SimpleArgument describes.

        If the actual content of SimpleArgument is Symbol,
        SymbolicArgumentException is raised.

        Returns
        -------
            Content of the Value of the SimpleArgument. If the SimpleArgument
            contains a Symbol, exception is raised.

        Raises
        ------
        SymbolicArgumentException
            If the actual content of SimpleArgument is Symbol.
        """

        if self._has_symbol():
            raise SymbolicArgumentException(
                f'SimpleArgument contains a Symbol: {self._content}.'
            )
        else:
            return self._content.value

    def _has_symbol(self) -> bool:
        return isinstance(self._content, Symbol)


class CompositeArgument(SymbolicArgument):
    """Subtype of SymbolicArgument combining several subarguments."""

    def _substitute_symbol_clean(self, symbol_now: Symbol, symbol_then: Symbol):
        """Do the symbol substitution with clean arguments.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `symbol_then` Symbol in the
            CompositeArgument.
        symbol_then
            Symbol which replaces the `symbol_now` Symbol in the
            CompositeArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. `symbol_now` was present in
            the CompositeArgument. False otherwise.
        """

        subarguments = self._get_sub_arguments()
        substitution_indicators = [
            sub_arg.substitute_symbol(symbol_now, symbol_then)
            for sub_arg in subarguments
        ]
        return any(substitution_indicators)

    def _substitute_value_clean(self, symbol_now: Symbol, value_then: Value):
        """Do the value substitution with clean arguments.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the `value_then` Value in the
            CompositeArgument.
        value_then
            Value which replaces the `symbol_now` Symbol in the
            CompositeArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. `symbol_now` was present in
            the CompositeArgument. False otherwise.
        """

        subarguments = self._get_sub_arguments()
        substitution_indicators = [
            sub_arg.substitute_value(symbol_now, value_then)
            for sub_arg in subarguments
        ]
        return any(substitution_indicators)

    def get_symbols(self) -> Iterable[Symbol]:
        """Return a list of Symbols which occur in the CompositeArgument.

        Returns
        -------
            A list of all symbols which occur in the CompositeArgument.
        """

        subarguments = self._get_sub_arguments()
        symbols_2d = [sub_arg.get_symbols() for sub_arg in subarguments]
        symbols_iter = itertools.chain(*symbols_2d)
        return set(symbols_iter)

    @abc.abstractmethod
    def get_actual_argument_value(self):
        """Return the value which the CompositeArgument describes.

        There must be no Symbol (i.e. free variable) in the CompositeArgument.

        Returns
        -------
            Real value described by the CompositeArgument.

        Raises
        ------
        SymbolicArgumentException
            If there are some Symbols left in the CompositeArgument.
        """

        pass

    @abc.abstractmethod
    def _get_sub_arguments(self) -> Iterable[SymbolicArgument]:
        """Return an iterable of SymbolicArguments which occur in the argument.

        Returns
        -------
            An iterable of all SymbolicArguments which occur in the
            CompositeArgument.
        """

        pass


class ListArgument(CompositeArgument):
    """Subtype of CompositeArgument for List of SymbolicArguments.

    The value of ListArgument is a list in which entries are occupied by the
    values of corresponding subarguments.
    """

    def __init__(self, *subarguments):
        """Create ListArgument of given subarguments.

        Parameters
        ----------
        subarguments
            SymbolicArguments which are subarguments of created ListArgument.
            Their values will follow the order in which the arguments were
            passed.

            Also, just one argument, sequence of SymbolicArguments, may be
            passed. Then the subarguments of ListArgument are extracted from
            the sequence.

        Notes
        -----
            The differentiation between one subargument and a sequence of
            subarguments, when just one value is passed, is on condition
            whether the value is subtype of SymbolicArgument.

            The test for being a sequence may appear to be wrong, in case a
            subtype of SymbolicArgument is also a sequence and the user
            wants to have it as a single subargument of a ListArgument.

            If more than one argument is passed, they must be subtypes of
            SymbolicArgument.
        """

        self._subarguments: List[SymbolicArgument]

        # If the only item in subarguments is to be considered as sequence
        # of the actual subarguments
        if len(subarguments) == 1 and \
                not isinstance(subarguments[0], SymbolicArgument):
            self._subarguments = [*subarguments[0]]
        else:
            # The subarguments sequence are the actual subarguments
            self._subarguments = list(subarguments)

        # Check type of subarguments
        for sub_arg in self._subarguments:
            if not isinstance(sub_arg, SymbolicArgument):
                raise TypeError(
                    'Subarguments of ListArgument must be instance of '
                    'SymbolicArgument'
                )

    def get_actual_argument_value(self) -> List:
        """Return the value which the ListArgument describes.

        A ListArgument is a list of values of its subarguments.

        Returns
        -------
            List of values of the ListArgument subarguments.

        Raises
        ------
        SymbolicArgumentException
            If there are some Symbols left in the ListArgument.
        """

        subargument_values = [sub_arg.get_actual_argument_value()
                              for sub_arg in self._subarguments]
        # The values are already in a list
        return subargument_values

    def _get_sub_arguments(self) -> Iterable[SymbolicArgument]:
        """Return an iterable of SymbolicArguments which occur in the argument.

        Returns
        -------
            An iterable of all SymbolicArguments which occur in the
            ListArgument.
        """

        return self._subarguments


class Symbol:
    """A single symbol in a SymbolicArgument."""

    def __init__(self, object_):
        self._object = object_


class Value:
    """A single value in a SymbolicArgument."""

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
