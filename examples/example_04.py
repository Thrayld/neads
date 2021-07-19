import collections

import neads as nd
from neads.utils import *
import neads.plugin_database as pl


def get_example(data_filename, grid):
    """Select 'coarse', 'medium' or 'fine' for the grid."""

    # Creating step for loading the data
    choice = get_single_node_choice(pl.csv_loader, data_filename,
                                    index_col='Date')
    loading = nd.ChoicesStep()
    loading.choices.append(choice)

    # Creating step for preprocessing
    choice = get_single_node_choice(pl.logarithmic_return)
    preprocessing = nd.ChoicesStep()
    preprocessing.choices.append(choice)

    # Creating step for evolution
    length, shift = get_interval_params(grid).values()
    separator = get_single_node_separator(pl.evolution_fix_window_length,
                                          length=length, shift=shift)
    extractor = get_single_node_extractor(pl.evolution_extractor)
    evolution = nd.DynamicStep(separator, extractor)

    # Creating step for building the network
    choice = get_single_node_choice(pl.pearson_correlation)
    building = nd.ChoicesStep()
    building.choices.append(choice)

    # Creating step for filtering the network
    choice = get_single_node_choice(pl.weight_threshold, 0.7)
    filtering = nd.ChoicesStep()
    filtering.choices.append(choice)

    # Creating step for final analysis of the network
    choice = get_single_node_choice(pl.average_clustering_coefficient)
    analyzing = nd.ChoicesStep()
    analyzing.choices.append(choice)

    # Putting it all to an instance of SCM
    scm = nd.SequentialChoicesModel()
    scm.steps.extend([loading, preprocessing, evolution, building, filtering,
                      analyzing])

    return scm


def get_interval_params(type_):
    if type_ == 'coarse':
        return {'length': 180, 'shift': 40}
    elif type_ == 'medium':
        return {'length': 180, 'shift': 20}
    elif type_ == 'fine':
        return {'length': 180, 'shift': 10}
    else:
        raise ValueError()

