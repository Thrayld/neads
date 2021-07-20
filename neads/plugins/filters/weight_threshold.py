import networkx as nx

from neads import Plugin, PluginID


def method(network, threshold):
    """Preserve only the edges whose weight is at least the threshold.

    Parameters
    ----------
    network
        The network whose edges are filtered.
    threshold
        The minimum weight of edge to stay in the network.

    Returns
    -------
        Unweighted network with edges whose weight was at least the
        threshold.
    """

    significant_edges = [(u, v) for u, v, e in network.edges(data=True)
                         if e['weight'] >= threshold]
    new_network = nx.Graph()
    new_network.add_nodes_from(network.nodes())
    new_network.add_edges_from(significant_edges)

    return new_network


weight_threshold = Plugin(PluginID('weight_threshold', 0), method)
