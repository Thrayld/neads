import unittest

from neads.activation_model import SymbolicArgumentSet


class _StandardAssertMethodsProvider(unittest.TestCase):
    def assertEqualArgSets(self, activation, plugin, /, *args, **kwargs):
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


tc = _StandardAssertMethodsProvider()

assertEqualArgSets = tc.assertEqualArgSets
