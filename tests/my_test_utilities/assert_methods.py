from __future__ import annotations

import unittest

from typing import TYPE_CHECKING

from neads.activation_model import SymbolicArgumentSet

if TYPE_CHECKING:
    from neads.sequential_choices_model.result_tree import ResultTree


class _StandardAssertMethodsProvider(unittest.TestCase):
    def assertArgSetsEqual(self, activation, plugin, /, *args, **kwargs):
        """Check equality of activation's arg set with the described set.

        Parameters
        ----------
        activation
            Activation whose SymbolicArgumentSet is compared.
        plugin
            Plugin for the other SymbolicArgumentSet.
        args
            Positional arguments for the other SymbolicArgumentSet.
        kwargs
            Keyword arguments for the other SymbolicArgumentSet.
        """

        expected = SymbolicArgumentSet(plugin, *args, **kwargs)
        actual = activation.argument_set
        self.assertEqual(expected, actual)

    def assertResultTreeEqual(self, expected: ResultTree, actual: ResultTree):
        """Check structural and data equality the given trees.

        Parameters
        ----------
        expected
            Expected tree.
        actual
            Actual tree.
        """

        self._assertSubtreeEqual(expected.root, actual.root)

    def _assertSubtreeEqual(self, expected, actual):
        self.assertEqual(expected.has_data, actual.has_data)
        if expected.has_data:
            self.assertEqual(expected.data, actual.data)

        self.assertEqual(len(expected.children), len(actual.children))
        for expected_child, actual_child in zip(expected.children,
                                                actual.children):
            self._assertSubtreeEqual(expected_child, actual_child)


tc = _StandardAssertMethodsProvider()

assertArgSetsEqual = tc.assertArgSetsEqual
assertResultTreeEqual = tc.assertResultTreeEqual
