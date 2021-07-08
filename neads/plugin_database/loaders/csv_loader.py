import pandas as pd

from neads import Plugin, PluginID


def method(_, filename, index_name=None) -> pd.DataFrame:
    """Compute a weighted networks using the Pearson correlation.
    The Pearson correlation of pairs of series defines the weights in
    the network.

    Parameters
    ----------
    _
        Formal parameter for use with SCM.
    filename
        Name of the csv file.
    index_name
        Name of the column which should be set as index. Value None indicates
        that there is no such column.

    Returns
    -------
        Loaded DataFrame from the csv file.
    """

    df = pd.read_csv(filename)
    if index_name is not None:
        df.set_index(index_name)

    return df


csv_loader = Plugin(PluginID('csv_loader', 0), method)
