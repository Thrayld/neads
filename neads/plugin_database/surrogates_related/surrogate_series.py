import numpy as np

from neads import Plugin, PluginID


def method(data, *, seed):
    """Compute surrogate time series to the given ones.

    Parameters
    ----------
    data : pandas.DataFrame
        Time series to be transformed into network.
    seed : int
        Whether the weights are normalized, so that the greatest absolute value
        is 1 (i.e. all entries are divided bz the greatest absolute value
        among all entries).
        Note, that then the values loses the units.

    Returns
    -------
        DataFrame whose columns contain surrogate time series corresponding
        to the original one.
    """

    result_data = data.apply(lambda x: get_single_ft_surrogate(x, seed))
    return result_data


surrogate_series = Plugin(PluginID('surrogate_series', 0), method)


# Original author: Nikola Jajcay, jajcay(at)cs.cas.cz
# https://github.com/jajcayn/multi-scale/blob/master/src/surrogates.py

# The docstring rewritten and the code edited to comply with the current best
# practices
def get_single_ft_surrogate(ts, seed):
    """Return single 1D Fourier transform surrogate of the given time series.

    Parameters
    ----------
    ts
        The time series whose surrogate will be generated.
    seed
        Seed for the numpy pseudorandom generator.
        If None, random seed is used.

    Returns
    -------
        Single 1D Fourier transform surrogate of the given time series.
    """

    generator = np.random.Generator(np.random.PCG64(seed))
    xf = np.fft.rfft(ts, axis=0)
    angle = generator.uniform(0, 2 * np.pi, (xf.shape[0],))
    # set the slowest frequency to zero, i.e. not to be randomised
    angle[0] = 0

    cxf = xf * np.exp(1j * angle)

    return np.fft.irfft(cxf, n=ts.shape[0], axis=0)
