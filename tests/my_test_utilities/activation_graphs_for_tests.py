
from neads.activation_model import SealedActivation, SealedActivationGraph

import tests.my_test_utilities.arithmetic_plugins as ar_plugins


def simple_tree():
    r"""Simple tree-shape graph.

    The graph is rooted tree without triggers.

          1
         / \
       2-   -3
      / \
    4-   -5
    https://textik.com/#8c3f6295aa9fed1d

    Returns
    -------
        A 2-tuple. First element is the graph, the second element the
        expected dict with results after evaluation.
    """

    ag = SealedActivationGraph()
    act_1 = ag.add_activation(ar_plugins.const, 10)
    act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 20)
    act_3 = ag.add_activation(ar_plugins.sub, act_1.symbol, 30)
    act_4 = ag.add_activation(ar_plugins.mul, act_2.symbol, 2)
    act_5 = ag.add_activation(ar_plugins.div, act_2.symbol, 5)

    results = {act_3: -20, act_4: 60, act_5: 6.}

    return ag, results


def simple_diamond():
    r"""Simple diamond-shape graph.

    The graph is diamond without triggers.

       1
      / \
    2-   -3
     \   /
      -4-
    https://textik.com/#dec70cf1132e783d

    Returns
    -------
        A 2-tuple. First element is the graph, the second element the
        expected dict with results after evaluation.
    """

    ag = SealedActivationGraph()
    act_1 = ag.add_activation(ar_plugins.const, 10)
    act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 20)
    act_3 = ag.add_activation(ar_plugins.sub, act_1.symbol, 30)
    act_4 = ag.add_activation(ar_plugins.mul, act_2.symbol, act_3.symbol)

    results = {act_4: -600}

    return ag, results


def simple_trigger_on_result():
    r"""Simple graph with a trigger-on-result method.

    The graph starts with one Activations with trigger-on-result which creates
    another three new Activations.

    1 -->
               1
              /|\
            2- | -4
               3
    https://textik.com/#96b8bda553fe103f

    Returns
    -------
        A 2-tuple. First element is the graph, the second element the
        expected dict with results after evaluation.
    """

    ag = SealedActivationGraph()
    act_1 = ag.add_activation(ar_plugins.const, 3)
    results = {}

    def act_1_trigger(data):
        created = []
        for idx in range(data):
            new_act = ag.add_activation(ar_plugins.pow,
                                        base=act_1.symbol, x=idx)
            created.append(new_act)
            results[new_act] = data**idx
        return created

    act_1.trigger_on_result = act_1_trigger

    return ag, results


def trigger_on_result_with_graph_trigger():
    r"""Graph with 2 trigger-on-result methods and graph's trigger.

    The graph starts with two Activations, both having a trigger-on-result
    which creates new Activations. Then the graph's trigger is invoked,
    and creates two Activations as children to all previously childless
    Activations (3 to 7).

    1  2 -->
                   1          2
                  /|\        / \
                3- | -5    6-   -7
                   4
    -->
        Activations 8, 9 for the bottom Activations

    Returns
    -------
        A 2-tuple. First element is the graph, the second element the
        expected dict with results after evaluation.
    """

    ag = SealedActivationGraph()
    act_1 = ag.add_activation(ar_plugins.const, 3)
    act_2 = ag.add_activation(ar_plugins.const, 2)
    results = {}

    def get_trigger(act):
        """Generate trigger for both Activations 1 and 2."""
        def act_trigger(data):
            created = []
            for idx in range(data):
                new_act = ag.add_activation(ar_plugins.pow,
                                            base=act.symbol, x=idx)
                created.append(new_act)
            return created

        return act_trigger

    act_1.trigger_on_result = get_trigger(act_1)
    act_2.trigger_on_result = get_trigger(act_2)

    def graph_trigger():
        childless_acts_symbols = [act.symbol
                                  for act in ag
                                  if len(act.children) == 0]
        act_8 = ag.add_activation(ar_plugins.min, *childless_acts_symbols)
        act_9 = ag.add_activation(ar_plugins.max, *childless_acts_symbols)
        results[act_8] = 1
        results[act_9] = 9
        return [act_8, act_9]

    ag.trigger_method = graph_trigger

    return ag, results

