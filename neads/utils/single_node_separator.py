from neads import ActivationGraph, Separator

# TODO: use in tests


def get_single_node_separator(plugin, /, *args, **kwargs):
    """Get separator with one node described by given arguments.

    But its first positional argument is the single graph's input!
    """

    ag = ActivationGraph(1)
    ag.add_activation(plugin, ag.inputs[0], *args, **kwargs)
    separator = Separator(ag)
    return separator
