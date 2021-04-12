from __future__ import annotations

from typing import Iterable, Union, List
import abc
import itertools


class SymbolicObjectException(Exception):
    pass


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
            Either two arguments `symbol_from` and object_to`.
            Or an iterable with the pairs `symbol_from`, `object_to` for
            multiple substitutions in one go.

        Returns
        -------
            SymbolicObject after substitution.

        Raises
        ------
        TypeError
            If the arguments do not respect the required types.
        """

        print('Aby se interpret neposral')
        raise NotImplementedError()
        # Check types
        # Check that Symbol is present
        # If it is, substitute

        # # Check the types of both arguments
        # if not isinstance(symbol_now, Symbol):
        #     raise TypeError(
        #         f"Argument 'symbol_now' has wrong type: {type(symbol_now)}"
        #     )
        # elif not isinstance(symbol_then, Symbol):
        #     raise TypeError(
        #         f"Argument 'symbol_then' has wrong type: {type(symbol_then)}"
        #     )
        #
        # return self._substitute_symbol_clean(symbol_now, symbol_then)

    @abc.abstractmethod
    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
        """Do the substitution with iterable of pairs for substitution.

        If a replacement occurs, new SymbolicObject is created from `self`,
        because SymbolicObject is immutable.

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
        """Return a list of Symbols which occur in the SymbolicObject.

        Returns
        -------
            A list of all symbols which occur in the SymbolicObject.
        """

        pass

    @abc.abstractmethod
    def get_value(self):
        """Return the object which the SymbolicObject describes.

        There must be no Symbol (i.e. free variable) in the SymbolicObject.

        Returns
        -------
            Object described by the SymbolicObject.

        Raises
        ------
        SymbolicObjectException
            If there are some Symbols left in the SymbolicObject.
        """

        # IDEA: return without copy
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
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            True, if the structure of both SymbolicObjects is the same and
            the Symbols are identical objects.
        """

        pass


# TODO: SimpleObject will be used no longer -- is replaced by Symbol and Value

# class SimpleObject(SymbolicObject):
#     """Subtype of SymbolicArgument containing a single Symbol or Value.
#
#     Elementary subtype of SymbolicArgument, which only contains a single
#     instance of Symbol or a single instance of Value. It effectively hides
#     operations with these basic building blocks.
#     """
#
#     def __init__(self, content: Union[Symbol, Value]):
#         """Create SimpleArgument with the given symbol.
#
#         Parameters
#         ----------
#         content
#             Symbol or Value, which is contained in the created SymbolicArgument.
#         """
#
#         if not isinstance(content, Symbol) and not isinstance(content, Value):
#             raise TypeError(
#                 f'Argument of SimpleArgument is neither Symbol nor Value: '
#                 f'{type(content)}'
#             )
#
#         self._content = content
#
#     def _substitute_symbol_clean(self, symbol_now: Symbol, symbol_then: Symbol):
#         """Do the symbol substitution with clean arguments.
#
#         Parameters
#         ----------
#         symbol_now
#             Symbol which is replaced by the `symbol_then` Symbol in the
#             SimpleArgument.
#         symbol_then
#             Symbol which replaces the `symbol_now` Symbol in the
#             SimpleArgument.
#
#         Returns
#         -------
#         bool
#             True, if any replacement occurred, i.e. symbol_now was present in
#             the SimpleArgument. False otherwise.
#         """
#
#         if self._has_symbol():
#             if self._content == symbol_now:
#                 # Substitution is possible
#                 self._content = symbol_then
#                 return True
#             else:
#                 # Symbol to be taken out is different from held symbol
#                 return False
#         else:
#             # SimpleArgument holds a Value, which cannot be substituted
#             return False
#
#     def _substitute_value_clean(self, symbol_now: Symbol, value_then: Value):
#         """Do the value substitution with clean arguments.
#
#         The replacement occur only if the `symbol_now` correspond to the
#         Symbol held by the SimpleArgument (in case it even holds a Symbol).
#
#         Parameters
#         ----------
#         symbol_now
#             Symbol which is replaced by the `value_then` Value in the
#             SimpleArgument.
#         value_then
#             Value which replaces the `symbol_now` Symbol in the
#             SimpleArgument.
#
#         Returns
#         -------
#         bool
#             True, if any replacement occurred, i.e. `symbol_now` was present in
#             the SimpleArgument. False otherwise.
#
#         Raises
#         ------
#         TypeError
#             If either of the arguments has a wrong type.
#         """
#
#         if self._has_symbol():
#             if self._content == symbol_now:
#                 # Substitution is possible
#                 self._content = value_then
#                 return True
#             else:
#                 # Symbol to be taken out is different from held symbol
#                 return False
#         else:
#             # SimpleArgument holds a Value, which cannot be substituted
#             return False
#
#     def get_symbols(self) -> Iterable[Symbol]:
#         """Return a list of Symbols which occur in the SymbolicArgument.
#
#         Returns
#         -------
#             A list of all symbols which occur in the SymbolicArgument.
#         """
#
#         if self._has_symbol():
#             # Symbol is the actual type of self._content
#             # Thus the type of return value correspond to type hint
#
#             # noinspection PyTypeChecker
#             return [self._content]
#         else:
#             return []
#
#     def get_actual_argument_value(self):
#         """Return the value which the SimpleArgument describes.
#
#         If the actual content of SimpleArgument is Symbol,
#         SymbolicArgumentException is raised.
#
#         Returns
#         -------
#             Content of the Value of the SimpleArgument. If the SimpleArgument
#             contains a Symbol, exception is raised.
#
#         Raises
#         ------
#         SymbolicArgumentException
#             If the actual content of SimpleArgument is Symbol.
#         """
#
#         if self._has_symbol():
#             raise SymbolicObjectException(
#                 f'SimpleArgument contains a Symbol: {self._content}.'
#             )
#         else:
#             return self._content.value
#
#     def _has_symbol(self) -> bool:
#         return isinstance(self._content, Symbol)


# TODO:
class CompositeObject(SymbolicObject):
    """Subtype of SymbolicObject combining several sub-objects."""

    @abc.abstractmethod
    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
        """Do the substitution with iterable of pairs for substitution.

        If a replacement occurs, new CompositeObject is created from `self`,
        because SymbolicObject is immutable.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            CompositeObject after substitution.
        """

        pass

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
    def get_value(self):
        """Return the object which the CompositeObject describes.

        There must be no Symbol (i.e. free variable) in the CompositeObject.

        Returns
        -------
            Object described by the CompositeObject.

        Raises
        ------
        SymbolicObjectException
            If there are some Symbols left in the CompositeObject.
        """

        pass

    @abc.abstractmethod
    def _get_sub_arguments(self) -> Iterable[SymbolicObject]:
        """Return an iterable of SymbolicObjects from which `self` is composed.

        Returns
        -------
            An iterable of all SymbolicObjects which occur in the
            CompositeObject.
        """

        pass

    @abc.abstractmethod
    def __eq__(self, other: SymbolicObject) -> bool:
        """Compare the CompositeObject with other SymbolicObject.

        Parameters
        ----------
        other
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            True, if the structure of both SymbolicObjects is the same and
            the Symbols are identical objects.
        """

        pass


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

        raise NotImplementedError()

        self._subobjects: List[SymbolicObject]

        # If the only item in subarguments is to be considered as sequence
        # of the actual subarguments
        if len(subobjects) == 1 and \
                not isinstance(subobjects[0], SymbolicObject):
            self._subobjects = [*subobjects[0]]
        else:
            # The subarguments sequence are the actual subarguments
            self._subobjects = list(subobjects)

        # Check type of subarguments
        for sub_arg in self._subobjects:
            if not isinstance(sub_arg, SymbolicObject):
                raise TypeError(
                    'Subarguments of ListArgument must be instance of '
                    'SymbolicArgument'
                )

    def _substitute_clean(self, substitution_pairs) -> SymbolicObject:
        """Do the substitution with iterable of pairs for substitution.

        If a replacement occurs, new ListObject is created from `self`,
        because SymbolicObject is immutable.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            ListObject whose entries are filled with sub-objects after
            substitution.
        """

        pass

    def get_value(self):
        """Return a list of values of sub-objects of the ListObject.

        There must be no Symbol (i.e. free variable) in the ListObject.

        Returns
        -------
            List of values of sub-objects of the ListObject.

        Raises
        ------
        SymbolicObjectException
            If there are some Symbols left in the CompositeObject.
        """

        pass

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

        pass

    # def get_actual_argument_value(self) -> List:
    #     """Return the value which the ListArgument describes.
    #
    #     A ListArgument is a list of values of its subarguments.
    #
    #     Returns
    #     -------
    #         List of values of the ListArgument subarguments.
    #
    #     Raises
    #     ------
    #     SymbolicArgumentException
    #         If there are some Symbols left in the ListArgument.
    #     """
    #
    #     subargument_values = [sub_arg.get_actual_argument_value()
    #                           for sub_arg in self._subobjects]
    #     # The values are already in a list
    #     return subargument_values

    def _get_sub_arguments(self) -> Iterable[SymbolicObject]:
        """Return an iterable of SymbolicArguments which occur in the argument.

        Returns
        -------
            An iterable of all SymbolicArguments which occur in the
            ListArgument.
        """

        return self._subobjects


class Symbol(SymbolicObject):
    """Symbol, i.e. free variable in a SymbolicObject."""

    def __init__(self):
        pass

    def _substitute_clean(self, substitution_pairs):
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
        pass

    def get_symbols(self) -> Iterable[Symbol]:
        """Return (`self`,) as the only symbol.

        Returns
        -------
            Return (`self`,) as the only symbol.
        """
        pass

    def get_value(self):
        """Raise exception as Symbol cannot be transferred to value.

        Raises
        ------
        SymbolicObjectException
            Symbol cannot be transferred to value.
        """
        pass

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

        pass


class Value(SymbolicObject):
    """Concrete value in a SymbolicObject."""

    def __init__(self, value):
        """Initialize Value with its content.

        The given object is copied in order to be able to maintain
        immutability of SymbolicObjects.

        Parameters
        ----------
        value
            Object which the Value held.
        """

        self._value = value

    def _substitute_clean(self, substitution_pairs):
        """Apply substitution on Value.

        No substitution can actually occur in Value, so always the original
        Value is returned.

        Parameters
        ----------
        substitution_pairs
            Iterable of pairs `symbol_from`, `object_to` for substitution.

        Returns
        -------
            `Self`, as no substitution can occur.
        """
        pass

    def get_symbols(self) -> Iterable[Symbol]:
        """Return empty tuple for Symbols in Value.

        Returns
        -------
            Empty tuple, as Value has no Symbols.
        """
        pass

    def get_value(self):
        """Return the actual value, which the Value contains.

        The value is copied in order to maintain immutability of Value as
        SymbolicObject in general. Thus, changes in the returned object do
        not affect the Value or any SymbolicObject in which is contained.

        Returns
        -------
            The actual value, which the Value contains.
        """
        pass

    def __eq__(self, other: SymbolicObject) -> bool:
        """Perform comparison of `self` with the other SymbolicObject.

        Parameters
        ----------
        other
            The other SymbolicObject, which is compared to `self`.

        Returns
        -------
            True, if the `other` is Value and object contained in `self` and
            `other` are value-equal (i.e. operator == is used). Otherwise False.
        """

        pass


