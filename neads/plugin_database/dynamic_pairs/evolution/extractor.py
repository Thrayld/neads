from neads import Plugin, PluginID


def method(df, intervals, index):
    """Select the given time interval of the time series.

    Parameters
    ----------
    df
        DataFrame with the time series.
    intervals
        Sequence intervals' boundaries. That is, each entry is a pair of
        indices. The first one is the first contained df's row, the second
        one is the first omitted df's row.
    index
        Index of the appropriate interval of the plugin realization.

    Returns
    -------
        Selection of rows by the given interval.
    """

    start, end = intervals[index]
    selection = df.iloc[start:end, :]
    return selection


evolution_extractor = Plugin(PluginID('evolution_extractor', 0), method)
