from __future__ import annotations

from typing import Union, Callable, Any
import collections.abc

from neads.plugin import Plugin
from neads.activation_model.symbolic_objects import Symbol
from neads.activation_model.symbolic_argument_set import SymbolicArgumentSet
from neads.activation_model.data_definition import DataDefinition


# IDEA: AG may incorporate another AG (with Symbol - Activation (or SO) mapping)

# IDEA: create Input class for graph's inputs for hiding Symbols to maintain
#  an API with good abstraction (a bit similar to Activation)

# IDEA: create a parser for Activation's arguments, which recognizes
#  structure of objects (for basic types) and presence of Activations (Inputs)
#  instead of -> ListObject(act_1.symbol, act_2.symbol)
#  we may write -> [act_1, act_2]

# IDEA: change NetworkX-like approach (all data in Graph) to OOP approach
#  (node data in nodes), see report from 11.5. for discussion

# IDEA: maybe add a shortcut to a set of all activations with trigger methods

class ActivationGraph(collections.abc.Iterable):
    """Capture dependencies among results of Plugins and graph's inputs.

    It is an acyclic data dependency graph which holds information how a result
    should be computed from some other results or from the graph's inputs.
    """

    def __init__(self, inputs_count):
        """Initialize a new ActivationGraph.

        Parameters
        ----------
        inputs_count
            Number of inputs of the graph.

        Raises
        ------
        ValueError
            If the inputs_count is less than 0.

        See Also
        --------
        SealedActivationGraph
            If you want to define graph with 0 inputs, SealedActivationGraph
            is probably a better choice.
        """

        if inputs_count < 0:
            raise ValueError(f'Inputs count must be at least 0: {inputs_count}')

        self._input_symbols = tuple(Symbol() for _ in range(inputs_count))
        self._trigger_method = None

        # Data structure for activations' data and for look up
        self._act_to_data: dict[
            Activation, ActivationGraph._ActivationData] = {}
        self._symbol_to_act: dict[Symbol, Activation] = {}
        self._plugin_argument_set_to_act: dict[
            tuple[Plugin, SymbolicArgumentSet], Activation] = {}

    @property
    def inputs(self) -> tuple[Symbol]:
        """Input symbols of the graph."""

        return self._input_symbols

    @property
    def trigger_method(self):
        """Graph's trigger method.

        The graph's trigger method is meant to be called when no other
        trigger method is present in the graph. That is, after all the
        trigger methods of all Activations have been called.

        The method must not add trigger methods to Activations except to
        those which creates.

        The one who calls the method must remove it from the graph at first.
        """

        return self._trigger_method

    @trigger_method.setter
    def trigger_method(
        self,
        trigger_method: Callable[[ActivationGraph], list[Activation]]
    ):
        """Set graph's trigger method.

        Raises
        ------
        ValueError
            If the graph already has a trigger.
        """

        self._arrange_trigger_set(self, '_trigger_method', trigger_method)

    @trigger_method.deleter
    def trigger_method(self):
        """Delete graph's trigger method.

        Raises
        ------
        ValueError
            If the graph does not carry a trigger method.
        """

        self._arrange_trigger_remove(self, '_trigger_method')

    def add_activation(
        self,
        plugin: Plugin,
        /,
        *args: object,
        **kwargs: object
    ) -> Activation:
        """Add Activation to the graph.

        A Plugin is passed followed by its positional and keyword arguments.

        Each of those arguments may be an actual object or just a description
        of one. Instances of SymbolicObject are regarded as the descriptions of
        the actual objects and they are processed correspondingly (i.e. their
        value is later extracted). Other instances are regarded as the actual
        arguments.

        The SymbolicObject instances may contain (and they usually do) Symbols
        of Activations from the graph or graph's inputs. The Symbols are
        placeholders for the results of those activations or inputs.

        Note that each argument needs to be hashable.

        Parameters
        ----------
        plugin
            Plugin which is supposed to process the actual arguments.
        args
            Positional arguments for the plugin. See the info above.
        kwargs
            Keyword arguments for the plugin. See the info above.

        Returns
        -------
            Activation of the graph, usually newly created.

            If an Activation with the same plugin and arguments exists,
            no Activation is created and the corresponding (already existing)
            Activation is returned.

        Raises
        ------
        TypeError
            If the plugin is not a Plugin.
            If the arguments for plugin do not fit its signature.
            If one of the arguments is not hashable.
        ValueError
            If there is an argument, which uses foreign Activation or foreign
            input symbol.
        """

        argument_set = self._get_clean_symbolic_argument_set(plugin, *args,
                                                             **kwargs)
        act = self._get_corresponding_activation(plugin, argument_set)
        return act

    def _get_clean_symbolic_argument_set(self, plugin, /, *args, **kwargs):
        """Create and return SAS for the arguments, while checking conditions.

        Parameters
        ----------
        plugin
            Plugin which is supposed to process the actual arguments.
        args
            Positional arguments for the plugin.
        kwargs
            Keyword arguments for the plugin.

        Returns
        -------
        SymbolicArgumentSet
            Argument set for the Activation. The return value is guaranteed
            to be clean is the sense that is built from objects satisfied the
            conditions below.

        Raises
        ------
        TypeError
            If the plugin is not a Plugin.
            If the arguments for plugin do not fit its signature.
            If one of the arguments is not hashable.
        ValueError
            If there is an argument, which uses foreign Activation or foreign
            input symbol.
        """

        if not isinstance(plugin, Plugin):
            raise TypeError(f"Plugin's type is invalid: {type(plugin)}")

        argument_set = SymbolicArgumentSet(plugin.signature, *args, **kwargs)
        try:
            hash(argument_set)
        except TypeError as e:
            raise TypeError('One of the arguments was not hashable.') from e
        self._check_arguments_symbols_are_from_the_graph(argument_set)

        return argument_set

    def _check_arguments_symbols_are_from_the_graph(
        self,
        argument_set: SymbolicArgumentSet
    ):
        """Check that all Symbols used in the argument set are from the graph.

        As 'Symbols from the graph' are considered Symbols of other activations
        and input Symbols of the graph.

        Parameters
        ----------
        argument_set
            Argument whose Symbols are going to be examined.

        Raises
        ------
        ValueError
            If there is a foreign Symbol.
        """

        for sym in argument_set.get_symbols():
            if sym not in self._symbol_to_act \
                    and sym not in self._input_symbols:
                raise ValueError('There is a foreign Symbol in the arguments')

    def _get_corresponding_activation(self, plugin, argument_set) -> Activation:
        """Return Activation described by arguments and create new, if needed.

        The method checks, whether such Activation exists in the graph. If it
        does, it is returned. If not, a new Activation is created and then
        returned.

        Parameters
        ----------
        plugin
            Plugin of the Activation.
        argument_set
            Argument set of the Activation.

        Returns
        -------
        Activation
            The Activation that corresponds to the given arguments.
        """

        # Try find the activation
        act_candidate = self._plugin_argument_set_to_act.get(
            (plugin, argument_set)
        )
        if act_candidate is None:
            # If there is not in the graph, create it
            return self._add_new_activation(plugin, argument_set)
        else:
            return act_candidate

    # TODO
    def _add_new_activation(self, plugin: Plugin,
                            argument_set: SymbolicArgumentSet) -> Activation:
        """Add a new activation to the graph and return it.

        Parameters
        ----------
        plugin
            Plugin of the activation.
        argument_set
            Argument set of the activation.

        Returns
        -------
            The new activation in the graph.
        """

        # Create activation objects
        activation = Activation(self)
        act_data = self._create_activation_data_object(plugin, argument_set)

        # Integrate activation of graph data structures
        self._act_to_data[activation] = act_data
        self._symbol_to_act[act_data.symbol] = activation
        self._plugin_argument_set_to_act[(plugin, argument_set)] = activation
        # self._definition_to_act[act_data.definition] = activation

        # Change state of other activations
        for parent in act_data.parents:
            self._act_to_data[parent].children.append(activation)

        return activation

    # TODO
    def _create_activation_data_object(self, plugin, argument_set) \
            -> _ActivationData:
        """Create data object of activation described by the arguments.

        Parameters
        ----------
        plugin
            Plugin of the activation.
        argument_set
            Argument set of the activation.

        Returns
        -------
            Data object (_ActivationData) corresponding to the given arguments.
        """

        # Create a Symbol
        symbol = Symbol()

        # Find parents and used inputs
        parents = []
        used_inputs = []
        for sym in argument_set.get_symbols():
            if None is not (parent := self._symbol_to_act.get(sym)):
                parents.append(parent)
            else:
                used_inputs.append(sym)  # The only other option

        # Compute level
        level = max(par.level for par in parents) + 1 if len(parents) else 0

        act_data = self._ActivationData(
            plugin=plugin,
            argument_set=argument_set,
            # definition=definition,
            symbol=symbol,
            parents=parents,
            level=level,
            used_inputs=used_inputs
        )
        return act_data

    def add_activation_trigger_on_result(
        self,
        activation,
        trigger_method: Callable[[Activation, Any], list[Activation]]
    ):
        """Add trigger-on-result method for the given Activation.

        The trigger-on-result method is meant to be called with the result data
        of the Activation.

        Its usual purpose is to add new Activations to the graph whose count
        depends on the computed data.

        The method must not add trigger methods to Activations except to
        those which creates.

        The one who calls the method must remove it from the graph at first.

        Parameters
        ----------
        activation
            Activation whose trigger-on-result method is added.
        trigger_method
            Trigger-on-result method for the Activation. The method takes the
            Activation and its result as arguments. Returns a list of newly
            created Activations.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph or if the
            Activation already has a trigger-on-result.
        """

        data = self._get_activation_data(activation)
        self._arrange_trigger_set(data, 'trigger_on_result', trigger_method)

    def remove_activation_trigger_on_result(self, activation):
        """Remove trigger-on-result method from the given Activation.

        Parameters
        ----------
        activation
            Activation whose trigger-on-result method is removed.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph or does not carry
            a trigger-on-result method.
        """

        data = self._get_activation_data(activation)
        self._arrange_trigger_remove(data, 'trigger_on_result')

    def add_activation_trigger_on_descendants(
        self,
        activation,
        trigger_method: Callable[[Activation], list[Activation]]
    ):
        """Add trigger-on-descendants method for the given Activation.

        The trigger-on-descendants method is meant to be called when no
        descendant of the Activation carries a trigger method (of either kind).
        That is, after all trigger methods of descendants of the Activation
        have been already called.

        Its usual purpose is to add gather results of its descendants in a
        common Activation, which was not possible to create right away
        due to presence of descendants' trigger methods.

        The method must not add trigger methods to Activations except to
        those which creates.

        The one who calls the method must remove it from the graph at first.

        Parameters
        ----------
        activation
            Activation whose trigger-on-descendants method is added.
        trigger_method
            Trigger-on-descendants method for the Activation. The method takes
            the Activation as a single argument. Returns a list of newly
            created Activations.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph or if the
            Activation already has a trigger-on-descendants.
        """

        data = self._get_activation_data(activation)
        self._arrange_trigger_set(data, 'trigger_on_descendants',
                                  trigger_method)

    def remove_activation_trigger_on_descendants(self, activation):
        """Remove trigger-on-descendants method from the given Activation.

        Parameters
        ----------
        activation
            Activation whose trigger-on-descendants method is removed.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph or does not carry
            a trigger-on-descendants method.
        """

        data = self._get_activation_data(activation)
        self._arrange_trigger_remove(data, 'trigger_on_descendants')

    def get_parents(self, activation) -> list[Activation]:
        """Return parents of the given Activation.

        Parents of an activation are those activations on whose result
        the original activation depends.

        Parameters
        ----------
        activation
            Activation whose parents are returned.

        Returns
        -------
            Parents of the given Activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.parents

    def get_used_inputs(self, activation) -> list[Symbol]:
        """Return graph's inputs used in arguments of the given Activation.

        Parameters
        ----------
        activation
            Activation whose graph's inputs are returned.

        Returns
        -------
            Graph's inputs used in arguments of the given Activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.used_inputs

    def get_children(self, activation) -> list[Activation]:
        """Return children of the given Activation.

        Children of an activation are those activations that depend on the
        result of original activation.

        Parameters
        ----------
        activation
            Activation whose children are returned.

        Returns
        -------
            Children of the given Activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.children

    def get_symbol(self, activation) -> Symbol:
        """Return symbol of the given Activation.

        Parameters
        ----------
        activation
            Activation whose symbol is returned.

        Returns
        -------
            Symbol of the given Activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.symbol

    def get_plugin(self, activation) -> Plugin:
        """Return plugin of the given Activation.

        Parameters
        ----------
        activation
            Activation whose plugin is returned.

        Returns
        -------
            Plugin of the given Activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.plugin

    def get_level(self, activation) -> int:
        """Return level of the given Activation in the graph.

        The level is determined as the maximum of levels of parents + 1.
        The Activations without parents have level 0.

        Parameters
        ----------
        activation
            The activation whose level is returned.

        Returns
        -------
            Level of the given Activation in the graph.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.level

    def get_argument_set(self, activation) -> SymbolicArgumentSet:
        """Return argument set of the given Activation.

        Parameters
        ----------
        activation
            Activation whose argument set is returned.

        Returns
        -------
            Argument set of the given Activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.argument_set

    def get_trigger_on_result(self, activation) -> Union[Callable, None]:
        """Return trigger-on-result method of the given Activation.

        Parameters
        ----------
        activation
            Activation whose trigger-on-result method set is returned.

        Returns
        -------
            Trigger-on-result method of the given Activation or None, if the
            Activation does not have one.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.trigger_on_result

    def get_trigger_on_descendants(self, activation) -> Union[Callable, None]:
        """Return trigger-on-descendants method of the given Activation.

        Parameters
        ----------
        activation
            Activation whose trigger-on-descendants method set is returned.

        Returns
        -------
            Trigger-on-descendants method of the given Activation or None, if
            the Activation does not have one.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        data = self._get_activation_data(activation)
        return data.trigger_on_descendants

    def __iter__(self):
        """Iterate over the Activations.

        Note that adding activation to the graph while iterating over the
        activations may result in undefined behavior.

        Returns
        -------
            An iterator over all Activations in the graph.
        """

        return iter(self._act_to_data)

    def _get_activation_data(self, activation: Activation):
        """Return activation data with check on activation presence in graph.

        Parameters
        ----------
        activation
            Activation which data is returned.

        Returns
        -------
            Activation data corresponding to the given activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        try:
            return self._act_to_data[activation]
        except KeyError as ex:
            raise ValueError(f'Activation does not belong to the graph: '
                             f'{activation}') from ex

    @staticmethod
    def _arrange_trigger_set(obj, attribute_trigger_name, new_trigger):
        """General method for setting trigger method while checking overrides.

        Parameters
        ----------
        obj
            Object which carries an attribute with trigger method.
        attribute_trigger_name
            Name of the attribute for trigger method.
        new_trigger
            New trigger method to be set.

        Raises
        ------
        RuntimeError
            If the trigger method already exists.
        """

        if getattr(obj, attribute_trigger_name) is not None:
            raise RuntimeError("Trigger method cannot be overridden.")
        else:
            setattr(obj, attribute_trigger_name, new_trigger)

    @staticmethod
    def _arrange_trigger_remove(obj, attribute_trigger_name):
        """General method for removing trigger method while checking existence.

        Parameters
        ----------
        obj
            Object which carries an attribute with trigger method.
        attribute_trigger_name
            Name of the attribute for trigger method.

        Raises
        ------
        RuntimeError
            If the object does not carry a trigger method.
        """

        if getattr(obj, attribute_trigger_name) is None:
            raise RuntimeError('There is no trigger method to delete.')
        else:
            setattr(obj, attribute_trigger_name, None)

    class _ActivationData:
        def __init__(self, *,
                     plugin: Plugin,
                     argument_set: SymbolicArgumentSet,
                     symbol: Symbol,
                     parents: list[Activation],
                     level: int,
                     used_inputs: list[Symbol]):
            self.plugin = plugin
            self.argument_set = argument_set
            self.symbol = symbol
            self.parents = parents
            self.level = level
            self.used_inputs = used_inputs

            # Newly created Activation does not have any children nor triggers
            self.children: list[Activation] = []
            self.trigger_on_result = None
            self.trigger_on_descendants = None


class SealedActivationGraph(ActivationGraph):
    """Capture dependencies among intermediate results of Plugins.

    The SealedActivationGraph differs from its parent class in presence of
    inputs. The SealedActivationGraph does not have any inputs. Thus,
    all intermediate results are fixed (sealed), not affected by graph's
    input (unlike in an ActivationGraph), which introduces extra options for
    treating the Activations.

    The most important difference is that the Activations have corresponding
    DataDefinition, which uniquely identify their results.
    """

    def __init__(self):
        """Initialize a new SealedActivationGraph."""

        super().__init__(0)
        self._definition_to_act: dict[DataDefinition, Activation] = {}

    # TODO: Add type hints that add activation produces SealedActivation
    def add_activation(
        self,
        plugin: Plugin,
        /,
        *args: object,
        **kwargs: object
    ) -> SealedActivation:
        # It very much depends on construction of the method in parent class
        # It is possible to just have the header here and the call reroutes
        # immediately to parent's add_activation

        return super().add_activation(plugin, *args, **kwargs)  # noqa

    def _get_corresponding_activation(self, plugin, argument_set) \
            -> SealedActivation:
        """Return Activation described by arguments and create new, if needed.

        The method checks, whether such Activation exists in the graph. If it
        does, it is returned. If not, a new Activation is created and then
        returned.

        Parameters
        ----------
        plugin
            Plugin of the Activation.
        argument_set
            Argument set of the Activation.

        Returns
        -------
        Activation
            The Activation that corresponds to the given arguments.
        """

        # TODO

    def get_definition(self, activation: SealedActivation) -> DataDefinition:
        """Return definition of the given Activation.

        Parameters
        ----------
        activation
            Activation whose definition is returned.

        Returns
        -------
            Definition of the given Activation.

        Raises
        ------
        ValueError
            If the Activation does not belong to the graph.
        """

        raise NotImplementedError()

    class _ActivationData(ActivationGraph._ActivationData):
        def __init__(self, *,
                     plugin: Plugin,
                     argument_set: SymbolicArgumentSet,
                     definition: DataDefinition,
                     symbol: Symbol,
                     parents: list[Activation],
                     level: int,
                     used_inputs: list[Symbol]):
            self.plugin = plugin
            self.argument_set = argument_set
            self.definition = definition
            self.symbol = symbol
            self.parents = parents
            self.level = level
            self.used_inputs = used_inputs

            # Newly created Activation does not have any children nor triggers
            self.children: list[Activation] = []
            self.trigger_on_result = None
            self.trigger_on_descendants = None


class Activation:
    """An individual Activation in an ActivationGraph.

    An Activation describes result of a Plugin called with a certain arguments.
    """

    def __init__(self, owner: ActivationGraph):
        """Initialize a new activation.

        Do NOT use this method directly for adding activations to a graph.
        USE graph.add_activation INSTEAD.

        Parameters
        ----------
        owner
            Graph to which the activation belong.
        """
        # IDEA: Should this method be protected by a guard?

        self._owner = owner

    @property
    def parents(self):
        """Return parents of the Activation.

        Parents of an activation are those activations on whose result
        the original activation depends.

        Returns
        -------
            Parents of the Activation.
        """

        return self._owner.get_parents(self)

    @property
    def used_inputs(self):
        """Return graph's inputs used in arguments of the Activation.

        Returns
        -------
            Graph's inputs used in arguments of the Activation.
        """

        return self._owner.get_used_inputs(self)

    @property
    def children(self):
        """Return children of the Activation.

        Children of an activation are those activations that depend on the
        result of original activation.

        Returns
        -------
            Children of the Activation.
        """

        return self._owner.get_children(self)

    @property
    def symbol(self):
        """Return symbol of the Activation.

        Returns
        -------
            Symbol of the Activation.
        """

        return self._owner.get_symbol(self)

    @property
    def plugin(self):
        """Return plugin of the Activation.

        Returns
        -------
            Plugin of the Activation.
        """

        return self._owner.get_plugin(self)

    @property
    def level(self):
        """Return level of the Activation in the graph.

        The level is determined as the maximum of levels of parents + 1.
        The Activations without parents have level 0.

        Returns
        -------
            Level of the Activation in the graph.
        """

        return self._owner.get_level(self)

    @property
    def argument_set(self):
        """Return argument set of the Activation.

        Returns
        -------
            Argument set of the Activation.
        """

        return self._owner.get_argument_set(self)

    @property
    def trigger_on_result(self):
        """Return trigger-on-result method of the Activation.

        Returns
        -------
            Trigger-on-result method of the Activation or None, if the
            Activation does not have one.
        """

        return self._owner.get_trigger_on_result(self)

    @trigger_on_result.setter
    def trigger_on_result(
        self,
        trigger_method: Callable[[Activation, Any], list[Activation]]
    ):
        """Add trigger-on-result method for the Activation.

        The trigger-on-result method is meant to be called with the result data
        of the Activation.

        Its usual purpose is to add new Activations to the owning graph whose
        count depends on the computed data.

        The method must not add trigger methods to Activations except to
        those which creates.

        The one who calls the method must remove it at first.

        Parameters
        ----------
        trigger_method
            Trigger-on-result method for the Activation. The method takes the
            Activation and its result as arguments. Returns a list of newly
            created Activations.

        Raises
        ------
        ValueError
            If the Activation already has a trigger-on-result.
        """

        self._owner.add_activation_trigger_on_result(self, trigger_method)

    @trigger_on_result.deleter
    def trigger_on_result(self):
        """Remove trigger-on-result method from the Activation.

        Raises
        ------
        ValueError
            If the Activation does not carry a trigger-on-result method.
        """

        self._owner.remove_activation_trigger_on_result(self)

    @property
    def trigger_on_descendants(self):
        """Return trigger-on-descendants method of the Activation.

        Returns
        -------
            Trigger-on-descendants method of the Activation or None, if the
            Activation does not have one.
        """

        return self._owner.get_trigger_on_descendants(self)

    @trigger_on_descendants.setter
    def trigger_on_descendants(
        self,
        trigger_method: Callable[[Activation], list[Activation]]
    ):
        """Add trigger-on-descendants method for the Activation.

        The trigger-on-descendants method is meant to be called when no
        descendant of the Activation carries a trigger method (of either kind).
        That is, after all trigger methods of descendants of the Activation
        have been already called.

        Its usual purpose is to add gather results of its descendants in a
        common Activation, which was not possible to create right away
        due to presence of descendants' trigger methods.

        The method must not add trigger methods to Activations except to
        those which creates.

        The one who calls the method must remove it from the graph at first.

        Parameters
        ----------
        trigger_method
            Trigger-on-descendants method for the Activation. The method takes
            the Activation as a single argument. Returns a list of newly
            created Activations.

        Raises
        ------
        ValueError
            If the Activation already has a trigger-on-descendants.
        """

        self._owner.add_activation_trigger_on_descendants(self, trigger_method)

    @trigger_on_descendants.deleter
    def trigger_on_descendants(self):
        """Remove trigger-on-descendants method from the Activation.

        Raises
        ------
        ValueError
            If the Activation does not carry a trigger-on-descendants method.
        """

        self._owner.remove_activation_trigger_on_descendants(self)


class SealedActivation(Activation):
    """An individual activation in an SealedActivationGraph.

    The SealedActivation is equipped with DataDefinition object which
    uniquely describes the resulting data of the activation.
    """

    def __init__(self, owner: SealedActivationGraph):
        """Initialize a new activation.

        Do NOT use this method directly for adding activations to a graph.
        USE `graph.add_activation` INSTEAD.

        Parameters
        ----------
        owner
            Graph to which the activation belong.
        """
        # IDEA: Should this method be protected by a guard?

        raise NotImplementedError()

    @property
    def definition(self):
        """Return definition of the SealedActivation.

        Only graphs without inputs have definitions for their activations.

        Returns
        -------
            Definition of the SealedActivation.
        """

        raise NotImplementedError()
