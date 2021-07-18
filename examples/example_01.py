import neads as nd
from neads.utils import get_single_node_choice
import neads.plugin_database as pl


def get_example(data_filename):
    # Creating step for loading the data
    choice = get_single_node_choice(pl.csv_loader, data_filename,
                                    index_col='Date')
    loading = nd.ChoicesStep()
    loading.choices.append(choice)

    # Creating step for preprocessing
    choice = get_single_node_choice(pl.logarithmic_return)
    preprocessing = nd.ChoicesStep()
    preprocessing.choices.append(choice)

    # Creating step for building the network
    choice = get_single_node_choice(pl.mutual_information)
    building = nd.ChoicesStep()
    building.choices.append(choice)

    # Creating step for filtering the network
    choice_a = get_single_node_choice(pl.planar_maximally_filtered_graph)
    choice_b = get_single_node_choice(pl.weight_threshold, 0.7)
    filtering = nd.ChoicesStep()
    filtering.choices.extend([choice_a, choice_b])

    # Creating step for final analysis of the network
    choice_a = get_single_node_choice(pl.average_clustering_coefficient)
    choice_b = get_single_node_choice(pl.average_degree)
    analyzing = nd.ChoicesStep()
    analyzing.choices.extend([choice_a, choice_b])

    # Putting it all to an instance of SCM
    scm = nd.SequentialChoicesModel()
    scm.steps.extend([loading, preprocessing, building, filtering, analyzing])

    return scm
