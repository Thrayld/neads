from __future__ import annotations

import inspect
from typing import Callable


class Plugin:
    """Class for main modularity block - the plugin.

    Plugin is a uniquely identified method which processes data and produces
    new one.
    """

    def __init__(self, plugin_id: PluginID, method: Callable):
        """Initialize a new Plugin with its ID and method.

        Parameters
        ----------
        plugin_id
            ID of the plugin. It is suppose to be unique and persistent among
            different runs of Neads.
        method
            The actual method of the plugin.

        Raises
        ------
        TypeError
            If the types does not fit.
        """

        if not isinstance(plugin_id, PluginID):
            raise TypeError(f'Given argument for Plugin ID is not of type '
                            f'PluginID: {plugin_id}')
        if not isinstance(method, Callable):
            raise TypeError(f'Given argument for method is not callable: '
                            f'{plugin_id}')

        self._plugin_id = plugin_id
        self._method = method

    @property
    def signature(self):
        """The signature of the Plugin."""
        return inspect.signature(self._method)

    @property
    def id(self):
        """The ID of the plugin."""
        return self._plugin_id

    def __call__(self, *args, **kwargs):
        """Call the method of the plugin with given arguments.

        Parameters
        ----------
        args
            Positional arguments for the plugin method.
        kwargs
            Key-word arguments for the plugin method.

        Returns
        -------
            Result of the plugin call with given arguments.

        Raises
        ------
        TypeError
            If the arguments do not match plugins signature.
        PluginException
        """

        # Throws TypeException if, the arguments does not fit
        self.signature.bind(*args, **kwargs)
        # If the bind passed, we call the method expecting arbitrary exception
        try:
            return self._method(*args, **kwargs)
        except Exception as e:
            raise PluginException('Plugin raised an exception.') from e


class PluginID:

    def __init__(self, name, version):
        self._name = name
        self._version = version

    def __eq__(self, other):
        if isinstance(other, PluginID):
            return self._name == other._name and self._version == other._version
        else:
            return False

    def __hash__(self):
        return hash((self._name, self._version))


class PluginException(Exception):
    pass