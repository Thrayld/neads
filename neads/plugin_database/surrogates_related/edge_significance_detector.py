from neads import Plugin, PluginID


def method(data_network, surrogate_networks, alpha=0.95, *, weight='weight'):
    """Return the data network with only the significant edges.

    The decision of edge significance goes as follows: first it is computed
    the number of corresponding edges whose weight is at most the weight of
    the data edge. Then, the edge is stays in the graph, if the number of the
    lighter edges divided by the number ALL edges (i.e. surrogates count + 1)
    is at most alpha.

    Parameters
    ----------
    data_network : networkx.Graph
        Weighted network created from the true data.
    surrogate_networks : list[networkx.Graph]
        Weighted networks created from the surrogate series. Their nodes must
        correspond to the nodes of the data_network.
    alpha : float
        Proportion of corresponding surrogates edges to surpass for the data
        edge, see the actual decision description above.
    weight
        Attribute to be used as weight.

    Returns
    -------
        The data network with only the significant edges.
    """

    result_network = data_network.copy()

    # Go though all edges and test one by one
    for u, v, data in data_network.edges(data=True):
        edge_weight = data[weight]
        greater_than = sum(edge_weight >= surr_net.get_edge_data(u, v)[weight]
                           for surr_net in surrogate_networks)
        greater_than_ratio = greater_than / (len(surrogate_networks) + 1)
        # Removes edge whose weight is too small
        if alpha >= greater_than_ratio:
            result_network.remove_edge(u, v)

    return result_network


edge_significance_detector \
    = Plugin(PluginID('edge_significance_detector', 0), method)
