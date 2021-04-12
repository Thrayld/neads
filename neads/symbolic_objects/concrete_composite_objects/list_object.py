from typing import Iterable

from neads.symbolic_objects.symbolic_object import SymbolicObject
from neads.symbolic_objects.composite_object import CompositeObject


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
            If there are some Symbols left in the ListObject.
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
        """Return an iterable of sub-objects which occur in the object.

        Returns
        -------
            An iterable of all sub-objects which occur in the ListObject.
        """

        pass
