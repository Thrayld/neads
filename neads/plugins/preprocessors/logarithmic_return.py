import numpy as np

from neads import Plugin, PluginID


def method(df):
    """Compute logarithmic return series of the time series.

    Parameters
    ----------
    df
        Time series whose logarithmic return series is computed.

    Returns
    -------
        The logarithmic return series of the given series.
    """

    log_ret = np.log(df) - np.log(df.shift(1))
    log_ret = log_ret.iloc[1:]  # without first row with NaNs
    return log_ret


logarithmic_return = Plugin(PluginID('logarithmic_return', 0), method)
