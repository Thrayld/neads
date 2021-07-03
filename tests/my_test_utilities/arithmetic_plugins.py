from neads.plugin import Plugin, PluginID

built_in_max = max
built_in_min = min
built_in_pow = pow


def _const(a):
    return a


def _add(a, b):
    return a + b


def _sub(a, b):
    return a - b


def _mul(a, b):
    return a * b


def _div(a, b):
    return a / b


def _max(*args):
    return built_in_max(*args)


def _min(*args):
    return built_in_min(*args)


def _pow(x, base=2):
    return base**x


const = Plugin(PluginID('const', 0), _const)
add = Plugin(PluginID('add', 0), _add)
sub = Plugin(PluginID('sub', 0), _sub)
mul = Plugin(PluginID('mul', 0), _mul)
div = Plugin(PluginID('div', 0), _div)
max = Plugin(PluginID('max', 0), _max)
min = Plugin(PluginID('min', 0), _min)
pow = Plugin(PluginID('pow', 0), _pow)
