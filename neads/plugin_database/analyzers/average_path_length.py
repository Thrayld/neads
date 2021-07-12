import networkx as nx
from statistics import mean
import itertools

from neads import Plugin, PluginID


def method(network):
    """Compute the average path length of the network.

    The length is computed only over reachable pairs.

    Parameters
    ----------
    network
        Network whose average path length is computed.

    Returns
    -------
        The average path length of the network.
    """

    # nx.all_pairs_shortest_path_length returns some cryptic iterator
    # Thus that much work with it
    source_target_dict = dict(nx.all_pairs_shortest_path_length(network))
    lists_of_lengths = [d.values() for d in source_target_dict.values()]
    flat_lengths = itertools.chain.from_iterable(lists_of_lengths)
    # For each s-t pair is their distance counted twice,
    # but it does not corrupt the mean
    return mean(flat_lengths)


average_path_length = Plugin(PluginID('average_path_length', 0), method)
