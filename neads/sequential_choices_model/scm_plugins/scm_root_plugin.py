from neads.activation_model.plugin import Plugin, PluginID


def _plugin_method():
    return None


root_plugin = Plugin(PluginID('scm_root_plugin', 0), _plugin_method)
