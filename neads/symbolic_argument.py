from __future__ import annotations

from typing import Iterable, Union, List
import abc
import itertools


class SymbolicObjectException(Exception):
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












