from neads import Plugin, PluginID


def method(df):
    """Compute relative change series of the time series.

    Parameters
    ----------
    df
        Time series whose relative change series is computed.

    Returns
    -------
        The relative change series of the given series.
    """

    relative_change_ = (df / df.shift(1)) - 1
    relative_change_ = relative_change_.iloc[1:]

    return relative_change_


relative_change = Plugin(PluginID('relative_change', 0), method)
