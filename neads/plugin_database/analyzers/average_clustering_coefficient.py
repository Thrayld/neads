import networkx as nx

from neads import Plugin, PluginID


average_clustering_coefficient = \
    Plugin(PluginID('average_clustering_coefficient', 0), nx.average_clustering)
