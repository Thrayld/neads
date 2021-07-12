import pandas as pd

from neads import Plugin, PluginID


def method(_, *args, **kwargs) -> pd.DataFrame:
    """Load the data using pandas' `read_csv` method.

    Parameters
    ----------
    _
        Formal parameter for use with SCM.
    args
        Positional arguments for `read_csv` (most notably the filename).
    kwargs
        Keyword arguments for `read_csv`.

    Returns
    -------
        Loaded DataFrame from the csv file.
    """

    df = pd.read_csv(*args, **kwargs)
    return df


csv_loader = Plugin(PluginID('read_csv', 0), method)

# import inspect
#
# sig = inspect.signature(pd.read_csv)
# new_param = inspect.Parameter('_', inspect.Parameter.POSITIONAL_ONLY)
# method_sig = sig.replace(parameters=[new_param, *sig.parameters.values()])
#
#
# def method(_, /, *args, **kwargs):
#     df = pd.read_csv(*args, **kwargs)
#     return df
#
#
# method.__signature__ = method_sig
