import numpy as np
import networkx as nx

from neads import Plugin, PluginID


def method(df, normalize):
    """Compute a weighted networks using the mutual information.

    The mutual information between pairs of series defines the weights in
    the network.

    Parameters
    ----------
    df : pandas.DataFrame
        Time series to be transformed into network.
    normalize : bool
        Whether the weights are normalized, so that the greatest value
        is 1. Note, that then the values loses their units.

    Returns
    -------
        Weighted network whose weights are determined by mutual information
        of the series of the adjacent nodes. The loops are removed.
    """

    mutual_info_matrix = df.corr(method=_mi)
    if normalize:
        max_entry = mutual_info_matrix.max().max()
        mutual_info_matrix = mutual_info_matrix / max_entry
    g = nx.from_pandas_adjacency(mutual_info_matrix)
    g.remove_edges_from(nx.selfloop_edges(g))

    return g


mutual_information = Plugin(PluginID('mutual_information', 0), method)


# Original author: Nikola Jajcay, jajcay(at)cs.cas.cz
# Some errors with new versions of numpy (such as indexing with float) were
# fixed, the docstring rewritten and the code split into several methods
def _mi(x, y, binning_algorithm='EQQ', bins=8, log2=True):
    """Compute mutual information between two time series x and y.

    We use the standard formula
        I(x; y) = sum( p(x,y) * log( p(x,y) / p(x)p(y) ),
    where p(x), p(y) and p(x, y) are probability distributions.

    For that, the probability distributions of both series needs to be
    estimated by some algorithm.

    We can use 'equiquantal binning', i.e. all bins should contain the same
    number of points. Further we can determine, whether the equiquantality is
    forced even if samples with the same value fall into different bins. Or
    whether we ensure that the same value samples fall into the same bin
    (while keeping the bins' sizes as leveled as possible).

    There is also equidistant binning which uses bins of the equal length.

        equidistant binning - algorithm keyword 'EQD'

        (preparing more...)

    Parameters
    ----------
    x
        The first time series.
    y
        The second time series.
    binning_algorithm
        Algorithm to determine bins for estimation of the distribution.
        Use 'EQQ' for forced equiquantal binning, 'EQQ2' for not-forced
        equiquantal binning (i.e. same values are in the same bin) or 'EQD'
        for equidistant binning.
    bins
        Bins count.
    log2
        Whether log2 will be used over natural logarithm. It determines
        units of the resulting mutual information. Bits for log2, nats for
        natural logarithm.

    Raises
    ------
    ValueError
        If the name of the binning algorithm is unknown to the method,
        i.e. different from 'EQQ', 'EQQ2', 'EQD'.
    """

    log_f = np.log2 if log2 else np.log

    if binning_algorithm == 'EQD':
        x_bins = bins
        y_bins = bins
        xy_bins = bins

    elif binning_algorithm == 'EQQ':
        x_bins = eqq_bins(x, bins)
        y_bins = eqq_bins(y, bins)
        xy_bins = [x_bins, y_bins]

    elif binning_algorithm == 'EQQ2':
        x_bins = eqq2_bins(x, bins)
        y_bins = eqq2_bins(y, bins)
        xy_bins = [x_bins, y_bins]
    else:
        raise ValueError(f'Invalid algorithm: {binning_algorithm}')

    # histograms
    count_x = np.histogramdd([x], bins=[x_bins])[0]
    count_y = np.histogramdd([y], bins=[y_bins])[0]
    count_xy = np.histogramdd([x, y], bins=xy_bins)[0]

    # normalise
    count_xy /= float(np.sum(count_xy))
    count_x /= float(np.sum(count_x))
    count_y /= float(np.sum(count_y))

    # sum
    mi = 0
    for i in range(bins):
        for j in range(bins):
            if count_x[i] != 0 and count_y[j] != 0 and count_xy[i, j] != 0:
                mi += count_xy[i, j] * log_f(
                    count_xy[i, j] / (count_x[i] * count_y[j]))

    return mi


def eqq_bins(x, bins):
    x_sorted = np.sort(x)
    x_bins = [x.min()]
    [x_bins.append(
        x_sorted[int(i * x.shape[0] / bins)]
    )
     for i in range(1, bins)]
    x_bins.append(x.max())

    return x_bins


def eqq2_bins(x, bins):
    x_sorted = np.sort(x)
    x_bins = [x.min()]
    one_bin_count = x.shape[0] / bins
    for i in range(1, bins):
        idx = i * one_bin_count
        if np.all(np.diff(x_sorted[idx - 1:idx + 2]) != 0):
            x_bins.append(x_sorted[idx])
        elif np.any(np.diff(x_sorted[idx - 1:idx + 2]) == 0):
            where = np.where(np.diff(x_sorted[idx - 1:idx + 2]) != 0)[0]
            expand_idx = 1
            while where.size == 0:
                where = np.where(np.diff(
                    x_sorted[idx - expand_idx:idx + 1 + expand_idx]) != 0)[
                    0]
                expand_idx += 1
            if where[0] == 0:
                x_bins.append(x_sorted[idx - expand_idx])
            else:
                x_bins.append(x_sorted[idx + expand_idx])
    x_bins.append(x.max())

    return x_bins
