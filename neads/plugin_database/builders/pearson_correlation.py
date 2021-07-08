from typing import TYPE_CHECKING

import networkx as nx

from neads import Plugin, PluginID

if TYPE_CHECKING:
    import pandas as pd


def method(data: pd.DataFrame):
    """Compute a weighted networks using the Pearson correlation.
    The Pearson correlation of pairs of series defines the weights in
    the network.

    Parameters
    ----------
    data
        Time series to be transformed into network.

    Returns
    -------
    networkx.Graph
        Weighted network whose weights are determined by Pearson
        correlation of the series of the adjacent nodes.
    """

    g = nx.from_pandas_adjacency(data.corr())
    g.remove_edges_from(nx.selfloop_edges(g))

    return g


pearson_correlation = Plugin(PluginID('pearson_correlation', 0), method)
