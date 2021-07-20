import networkx as nx

from neads import Plugin, PluginID


def method(network):
    """Compute unweighted PMFG over the network.

    The Planar Maximally Filtered Graph is the planar graph whose edges
    are selected by a greedy algorithm. That is, the edges with greatest
    weight are added one by one to an empty graph while preserving its
    planarity.

    Parameters
    ----------
    network
        The network whose PMFG is computed.

    Returns
    -------
        PMFG of the given network. The edges has no weight.
    """

    pmfg = nx.Graph()  # Nodes will be added via edges; surely each deg(v) > 0
    for source, dest, data in _get_sorted_edges(network):
        pmfg.add_edge(source, dest)
        is_planar, _ = nx.check_planarity(pmfg)
        if not is_planar:
            pmfg.remove_edge(source, dest)

        if len(pmfg.edges()) == 3 * (len(pmfg.nodes) - 2):
            # Theoretical maximum (by Euler's formula) is reached
            break

    return pmfg


def _get_sorted_edges(G):
    return sorted(
        G.edges(data=True),
        key=lambda x: x[2]['weight'],
        reverse=True
    )


planar_maximally_filtered_graph = \
    Plugin(PluginID('planar_maximally_filtered_graph', 0), method)
