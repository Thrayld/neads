from neads.activation_model import ActivationGraph


def get_result_activation(graph: ActivationGraph):
    """Check that the graph has exactly one result Activation and return it.

    Activation is regarded as the 'result Activation' iff it is childless.

    Parameters
    ----------
    graph
        The graph whose result Activation is returned.

    Returns
    -------
        The result Activation of the given graph.

    Raises
    ------
    ValueError
        If the graph does not have exactly one result Activation.
    """

    result_acts = [act for act in graph if not act.children]
    if len(result_acts) == 1:
        return result_acts[0]
    else:
        raise ValueError(
            f'The graph does not have one result Activation: {result_acts}'
        )

