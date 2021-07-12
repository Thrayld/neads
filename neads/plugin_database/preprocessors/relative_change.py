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

    relative_changes = (df - df.shift(1)) / df.shift(1)
    relative_changes = relative_changes.iloc[1:]

    return relative_changes


relative_change = Plugin(PluginID('relative_change', 0), method)
