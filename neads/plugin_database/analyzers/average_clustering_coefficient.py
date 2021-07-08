import networkx as nx

from neads import Plugin, PluginID


def method(network):
    """Computes the average clustering coefficient of the network.
    Parameters
    ----------
    network
        Network whose average clustering coefficient is computed.
    Returns
    -------
        The average clustering coefficient of the network.
    """

    av_cc = nx.average_clustering(network)

    return av_cc


average_clustering_coefficient = Plugin(PluginID('average_degree', 0), method)
