from neads import ActivationGraph, Choice

# TODO: use in tests


def get_single_node_choice(plugin, /, *args, **kwargs):
    """Get choice with one node described by given arguments.

    But its first positional argument is the single graph's input!
    """

    ag = ActivationGraph(1)
    ag.add_activation(plugin, ag.inputs[0], *args, **kwargs)
    choice = Choice(ag)
    return choice
