from statistics import mean

from neads import Plugin, PluginID


def method(network):
    """Computes the average degree of the network.

    Parameters
    ----------
    network
        Network whose average degree is computed.

    Returns
    -------
        The average degree of the network.
    """

    degrees = dict(network.degree()).values()
    av_deg = mean(degrees)

    return av_deg


average_degree = Plugin(PluginID('average_degree', 0), method)
