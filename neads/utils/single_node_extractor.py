from neads import ActivationGraph, Extractor

# TODO: use in tests


def get_single_node_extractor(plugin, /, *args, **kwargs):
    """Get extractor with one node described by given arguments.

    But its first three positional arguments are the graph's inputs!
    """

    ag = ActivationGraph(3)
    ag.add_activation(plugin, *ag.inputs, *args, **kwargs)
    extractor = Extractor(ag)
    return extractor
