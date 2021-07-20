import neads as nd
from neads.utils import get_single_node_choice
import neads.plugins as pl


def get_example(data_filename):
    # Creating step for loading the data
    choice = get_single_node_choice(pl.read_csv, data_filename,
                                    index_col='Date')
    loading = nd.ChoicesStep()
    loading.choices.append(choice)

    # Creating step for preprocessing
    choice = get_single_node_choice(pl.logarithmic_return)
    preprocessing = nd.ChoicesStep()
    preprocessing.choices.append(choice)

    # Hand-made choice using surrogate series for detecting the edges
    ag = nd.ActivationGraph(1)
    # Creating surrogate time series and their networks
    surr_network_symbols = []
    for idx in range(99):
        surr = ag.add_activation(pl.surrogate_series, ag.inputs[0], seed=idx)
        net = ag.add_activation(pl.mutual_information, surr.symbol)
        surr_network_symbols.append(net.symbol)
    # Creating data network
    data_network = ag.add_activation(pl.mutual_information, ag.inputs[0])
    # Creating the result node, which makes the detection of edges
    surr_network_arg = nd.ListObject(*surr_network_symbols)
    ag.add_activation(pl.edge_significance_detector,
                      data_network.symbol, surr_network_arg)

    # Create the choice and the step
    choice = nd.Choice(ag)
    building = nd.ChoicesStep()
    building.choices.append(choice)

    # Putting it all to an instance of SCM
    scm = nd.SequentialChoicesModel()
    scm.steps.extend([loading, preprocessing, building])

    return scm
