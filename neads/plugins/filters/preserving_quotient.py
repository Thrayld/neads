import networkx as nx

from neads import Plugin, PluginID


def method(network, quotient):
    """Preserve only the given quotient of weightiest edges in the network.

    The other edges are removed. Weight of the existent edges is set to 1.

    Parameters
    ----------
    network
        The network whose edges are filtered.
    quotient
        The ratio of edges to stay.

    Returns
    -------
        Unweighted network with only a given quotient of edges.
    """

    sorted_edges = sorted(
        network.edges(data=True),
        key=lambda e: e[2]['weight'],
        reverse=True
    )
    significant_edges = sorted_edges[:int(quotient*len(sorted_edges))]
    new_network = nx.Graph()
    new_network.add_nodes_from(network.nodes())
    new_network.add_edges_from((u, v) for u, v, d in significant_edges)

    return new_network


preserving_quotient = Plugin(PluginID('preserving_quotient', 0), method)
