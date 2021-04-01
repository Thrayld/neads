from __future__ import annotations

from typing import Iterable, Union
import abc


class SymbolicArgumentException(Exception):
    pass


class SymbolicArgument(abc.ABC):
    """Capture syntactic shape of an argument.

    Support substitution for individual Symbols (i.e. variables). If the
    SymbolicArgument is without Symbols, it can be transformed into the real
    argument.
    """

    @abc.abstractmethod
    def substitute_symbol(self, symbol_now: Symbol, symbol_then: Symbol):
        """Substitute a Symbol for one of current Symbols.

        The substitution is propagated to all the sub-arguments.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the *symbol_then* Symbol in the
            SymbolicArgument.
        symbol_then
            Symbol which replaces the *symbol_now* Symbol in the
            SymbolicArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. symbol_now was present in
            the SymbolicArgument. False otherwise.
        """

        pass

    @abc.abstractmethod
    def substitute_value(self, symbol_now: Symbol, value_then: Value):
        """Substitute a Value for one of current Symbols.

        The substitution is propagated to all the sub-arguments.

        Parameters
        ----------
        symbol_now
            Symbol which is replaced by the *value_then* Value in the
            SymbolicArgument.
        value_then
            Value which replaces the *symbol_now* Symbol in the
            SymbolicArgument.

        Returns
        -------
        bool
            True, if any replacement occurred, i.e. symbol_now was present in
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
        """Return the value which the SyntacticArgument describes.

        There must be no Symbol (i.e. free variable) in the SyntacticArgument.

        Returns
        -------
            Real value described by the SyntacticArgument
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

        self._content = content

    def substitute_symbol(self, symbol_now: Symbol, symbol_then: Symbol):
        """Substitute a Symbol for the given Symbol.

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

        # Check the types of both arguments
        if not isinstance(symbol_now, Symbol):
            raise TypeError(
                f"Argument 'symbol_now' has wrong type: {type(symbol_now)}"
            )
        elif not isinstance(symbol_then, Symbol):
            raise TypeError(
                f"Argument 'symbol_then' has wrong type: {type(symbol_then)}"
            )

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

    def substitute_value(self, symbol_now: Symbol, value_then: Value):
        """Substitute a Value for the given Symbol.

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

        # Check the types of both arguments
        if not isinstance(symbol_now, Symbol):
            raise TypeError(
                f"Argument 'symbol_now' has wrong type: {type(symbol_now)}"
            )
        elif not isinstance(value_then, Value):
            raise TypeError(
                f"Argument 'value_then' has wrong type: {type(value_then)}"
            )

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







class Symbol:
    """A single symbol in a SymbolicArgument."""

    def __init__(self, object):
        self._object = object


class Value:
    """A single value in a SymbolicArgument."""

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
