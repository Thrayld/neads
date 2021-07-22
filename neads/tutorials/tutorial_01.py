import neads as nd
from neads.utils import get_single_node_choice
import neads.plugins as pl


def get_graph(data_filename):
    # Creating step for loading the data
    choice = get_single_node_choice(pl.read_csv, data_filename,
                                    index_col='Date')
    loading = nd.ChoicesStep()
    loading.choices.append(choice)

    # Creating step for preprocessing
    choice = get_single_node_choice(pl.logarithmic_return)
    preprocessing = nd.ChoicesStep()
    preprocessing.choices.append(choice)

    # Creating step for building the network
    choice = get_single_node_choice(pl.pearson_correlation)
    building = nd.ChoicesStep()
    building.choices.append(choice)

    # Creating step for filtering the network
    choice_a = get_single_node_choice(pl.weight_threshold, 0.6)
    choice_b = get_single_node_choice(pl.planar_maximally_filtered_graph)
    filtering = nd.ChoicesStep()
    filtering.choices.extend([choice_a, choice_b])

    # Creating step for final analysis of the network
    choice_a = get_single_node_choice(pl.average_degree)
    choice_b = get_single_node_choice(pl.average_clustering_coefficient)
    analyzing = nd.ChoicesStep()
    analyzing.choices.extend([choice_a, choice_b])

    # Putting it all to an instance of SCM
    scm = nd.SequentialChoicesModel()
    scm.steps.extend([loading, preprocessing, building, filtering, analyzing])

    graph = scm.create_graph()
    return graph
